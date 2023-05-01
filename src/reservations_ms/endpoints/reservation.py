import asyncio
import json
import logging
from datetime import datetime

from fastapi import APIRouter, status
from pydantic import BaseModel
from starlette.responses import JSONResponse, Response

from mongodb.mongodb_client import MongoDBClient, TRIPS_DOCUMENT_ID
from rabbitmq.rabbitmq_client import RabbitMQClient, PURCHASES_EXCHANGE_NAME, \
    RESERVATIONS_EXCHANGE_NAME, RESERVATIONS_PUBLISH_QUEUE_NAME, \
    PURCHASES_PUBLISH_QUEUE_NAME, PAYMENTS_PUBLISH_QUEUE_NAME, PAYMENTS_EXCHANGE_NAME
from service.expiration_handler import start_measuring_reservation_time

router = APIRouter(prefix="/api/v1/reservation")

logger = logging.getLogger("reservations")


class TripReservationData(BaseModel):
    hotel_id: str
    room_type: str
    connection_id: str


@router.post("/{trip_offer_id}",
             responses={
                 201: {"description": "Reservation successfully created"},
                 404: {"description": "Trip with provided ID does not exist"},
                 500: {"description": "Unknown error occurred"}
             },
             )
async def make_reservation(trip_offer_id: str, payload: TripReservationData):
    """
    Create a trip reservation
    """
    current_os_time = datetime.now()
    current_datetime = current_os_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
    try:
        logger.info(f"Reservation creation process for offer {trip_offer_id} started at {current_datetime}")
        trips_document = MongoDBClient.trips_collection.find_one({"_id": TRIPS_DOCUMENT_ID})
        if trips_document is None:
            logger.info(f"Trip offers database is empty")
            return Response(status_code=status.HTTP_404_NOT_FOUND,
                            content=f"Trip with ID {trip_offer_id} does not exist",
                            media_type="text/plain")
        if trip_offer_id not in trips_document["trip_offers"]:
            logger.info(f"From available trip offers {trips_document} there is no value {trip_offer_id}")
            return Response(status_code=status.HTTP_404_NOT_FOUND,
                            content=f"Trip with ID {trip_offer_id} does not exist",
                            media_type="text/plain")

        init_doc = {
            "trip_offer_id": trip_offer_id,
            "reservation_status": "temporary",
            "reservation_creation_time": current_datetime,
            "uid": "example_uid"
        }
        insert_result = MongoDBClient.reservations_collection.insert_one(document=init_doc)
        reservation_id = str(insert_result.inserted_id)

        expiration_timer_task = asyncio.create_task(start_measuring_reservation_time(
            reservation_id=reservation_id,
            reservation_creation_time=current_datetime))

        client = RabbitMQClient()
        client.send_data_to_queue(queue_name=PURCHASES_PUBLISH_QUEUE_NAME,
                                  exchange_name=PURCHASES_EXCHANGE_NAME,
                                  payload=json.dumps({
                                      "title": "reservation_creation",
                                      "_id": reservation_id,
                                      "trip_offer_id": trip_offer_id,
                                  }, ensure_ascii=False).encode('utf-8'))

        client.send_data_to_queue(queue_name=RESERVATIONS_PUBLISH_QUEUE_NAME,
                                  exchange_name=RESERVATIONS_EXCHANGE_NAME,
                                  payload=json.dumps({
                                      "title": "reservation_status_update",
                                      "trip_offer_id": trip_offer_id,
                                      "reservation_id": reservation_id,
                                      "reservation_status": "created",
                                      "hotel_id": payload.hotel_id,
                                      "room_type": payload.room_type,
                                      "connection_id": payload.connection_id,
                                  }, ensure_ascii=False).encode('utf-8'))

        client.send_data_to_queue(queue_name=PAYMENTS_PUBLISH_QUEUE_NAME, exchange_name=PAYMENTS_EXCHANGE_NAME,
                                  payload=json.dumps({
                                      "title": "reservation_creation_time",
                                      "_id": reservation_id,
                                      "reservation_creation_time": current_datetime
                                  }, ensure_ascii=False).encode('utf-8'))
        client.close_connection()

        logger.info(f"Reservation with ID {reservation_id} created.")
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"reservation_id": reservation_id},
                            media_type="application/json")
    except Exception as ex:
        logger.info(f"Exception in reservation ms occurred: {ex}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
