import asyncio
import json
import logging

import requests
from fastapi import APIRouter, status
from starlette.responses import JSONResponse, Response

from mongodb.mongodb_client import MongoDBClient, TRIPS_DOCUMENT_ID
from rabbitmq.rabbitmq_client import RabbitMQClient, PURCHASES_EXCHANGE_NAME, \
    RESERVATIONS_EXCHANGE_NAME, RESERVATIONS_PUBLISH_QUEUE_NAME, \
    PURCHASES_PUBLISH_QUEUE_NAME, PAYMENTS_PUBLISH_QUEUE_NAME, PAYMENTS_EXCHANGE_NAME
from service.expiration_handler import start_measuring_reservation_time

router = APIRouter(prefix="/api/v1/reservation")

logger = logging.getLogger("reservations")


@router.post("/{trip_id}",
             responses={
                 201: {"description": "Reservation successfully created"},
                 404: {"description": "Trip with provided ID does not exist"},
                 500: {"description": "Unknown error occurred"}
             },
             )
async def make_reservation(trip_id: str):
    """
    Create a trip reservation
    """

    current_time_response = requests.get(url="https://timeapi.io/api/Time/current/zone?timeZone=Europe/Warsaw")
    current_datetime = json.loads(current_time_response.text)["dateTime"][:-1]
    init_doc = {
        "trip_id": trip_id,
        "reservation_status": "temporary",
        "reservation_creation_time": current_datetime,
        "uid": "example_uid"
    }
    try:
        trips_document = MongoDBClient.trips_collection.find_one({"_id": TRIPS_DOCUMENT_ID})
        if trips_document is None:
            logger.info(f"Trips database is empty")
            return Response(status_code=status.HTTP_404_NOT_FOUND, content=f"Trip with ID {trip_id} does not exist",
                            media_type="text/plain")
        if trip_id not in trips_document["trips"]:
            logger.info(f"From available trips {trips_document} there is no value {trip_id}")
            return Response(status_code=status.HTTP_404_NOT_FOUND, content=f"Trip with ID {trip_id} does not exist",
                            media_type="text/plain")

        insert_result = MongoDBClient.reservations_collection.insert_one(document=init_doc)

        expiration_timer_task = asyncio.create_task(start_measuring_reservation_time(
            reservation_id=str(insert_result.inserted_id),
            reservation_creation_time=current_datetime))

        client = RabbitMQClient()
        client.send_data_to_queue(queue_name=PURCHASES_PUBLISH_QUEUE_NAME,
                                  exchange_name=PURCHASES_EXCHANGE_NAME,
                                  payload=json.dumps({
                                      "_id": str(insert_result.inserted_id),
                                      "trip_id": trip_id,
                                  }, ensure_ascii=False).encode('utf-8'))

        client.send_data_to_queue(queue_name=RESERVATIONS_PUBLISH_QUEUE_NAME,
                                  exchange_name=RESERVATIONS_EXCHANGE_NAME,
                                  payload=json.dumps({
                                      "trip_id": trip_id,
                                      "reservation_status": "created",
                                  }, ensure_ascii=False).encode('utf-8'))

        client.send_data_to_queue(queue_name=PAYMENTS_PUBLISH_QUEUE_NAME, exchange_name=PAYMENTS_EXCHANGE_NAME,
                                  payload=json.dumps({
                                      "_id": str(insert_result.inserted_id),
                                      "reservation_creation_time": current_datetime
                                  }, ensure_ascii=False).encode('utf-8'))
        client.close_connection()

        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"reservation_id": str(insert_result.inserted_id)},
                            media_type="application/json")
    except Exception as ex:
        logger.info(f"Exception in reservation ms occurred: {ex}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
