import json
import logging
from datetime import datetime

from fastapi import APIRouter, status
from mongodb.mongodb_client import MongoDBClient, TRIPS_DOCUMENT_ID
from starlette.responses import JSONResponse, Response

from rabbitmq.rabbitmq_client import RabbitMQClient, PURCHASES_EXCHANGE_NAME, \
    RESERVATIONS_EXCHANGE_NAME, RESERVATIONS_PUBLISH_QUEUE_NAME, \
    PURCHASES_PUBLISH_QUEUE_NAME, PAYMENTS_PUBLISH_QUEUE_NAME, PAYMENTS_EXCHANGE_NAME

router = APIRouter(prefix="/api/v1/reservation")
# logging.basicConfig(
#         format="%(levelname)s %(asctime)-4s %(message)s",
#         level=logging.INFO,
#         datefmt="%Y-%m-%d %H:%M:%S",
#     )
logger = logging.getLogger("reservations")


@router.post("/{trip_id}",
             responses={
                 201: {"description": "Reservation successfully created"},
                 404: {"description": "Trip with provided ID does not exist"},
                 422: {"description": "Unknown error occurred"}
             },
             )
async def make_reservation(trip_id: str):
    """
    Create a trip reservation
    """

    current_time = datetime.now().strftime("%Y-%m-%d:%H:%M:%S")
    init_doc = {
        "trip_id": trip_id,
        "reservation_status": "temporary",
        "reservation_creation_time": current_time,
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

        purchases_client = RabbitMQClient()
        purchases_client.send_data_to_queue(queue_name=PURCHASES_PUBLISH_QUEUE_NAME,
                                            exchange_name=PURCHASES_EXCHANGE_NAME,
                                            payload=json.dumps({
                                                "_id": str(insert_result.inserted_id),
                                                "reserved": True
                                            }, ensure_ascii=False).encode('utf-8'))
        purchases_client.close_connection()

        reservations_client = RabbitMQClient()
        reservations_client.send_data_to_queue(queue_name=RESERVATIONS_PUBLISH_QUEUE_NAME,
                                               exchange_name=RESERVATIONS_EXCHANGE_NAME,
                                               payload=json.dumps({
                                                   "trip_id": trip_id,
                                                   "reserved": True,
                                               }, ensure_ascii=False).encode('utf-8'))
        reservations_client.close_connection()

        payments_client = RabbitMQClient()
        payments_client.send_data_to_queue(queue_name=PAYMENTS_PUBLISH_QUEUE_NAME, exchange_name=PAYMENTS_EXCHANGE_NAME,
                                           payload=json.dumps({
                                               "_id": str(insert_result.inserted_id),
                                               "reservation_creation_time": current_time
                                           }, ensure_ascii=False).encode('utf-8'))
        payments_client.close_connection()

        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"reservation_id": str(insert_result.inserted_id)},
                            media_type="application/json")
    except Exception as ex:
        raise ex
