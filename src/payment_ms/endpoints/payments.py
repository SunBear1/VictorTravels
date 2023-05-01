import json
import logging
import random
from datetime import datetime

import bson.errors
from bson import ObjectId
from fastapi import APIRouter, status
from starlette.responses import JSONResponse, Response

from mongodb.mongodb_client import MongoDBClient
from rabbitmq.rabbitmq_client import RabbitMQClient, PURCHASES_PUBLISH_QUEUE_NAME, PURCHASES_EXCHANGE_NAME

router = APIRouter(prefix="/api/v1/payment")

logger = logging.getLogger("payments")

RESERVATION_EXPIRE_TIME = 180
CHANCE_OF_FAILING_PAYMENT = 4


@router.post("/{reservation_id}",
             responses={
                 200: {"description": "Payment performed successfully"},
                 404: {"description": "Reservation with provided ID does not exist"},
                 400: {"description": "Reservation with provided ID has already been paid for"},
                 410: {"description": "Reservation with ID has expired"},
                 402: {"description": "Payment for reservation have failed"},
                 500: {"description": "Unknown error occurred"}
             },
             )
async def make_payment(reservation_id: str):
    """
    Handle payment for a specific trip offer reservation
    """

    try:
        logger.info(f"Payment process for reservation {reservation_id} started.")
        purchase_doc = MongoDBClient.payments_collection.find_one({"_id": ObjectId(reservation_id)})
        if purchase_doc is None or purchase_doc["purchase_status"] == "pending":
            logger.info(f"There is no information about the reservation {reservation_id} purchase")
            return Response(status_code=status.HTTP_404_NOT_FOUND,
                            content=f"Reservation with ID {reservation_id} has not been purchased",
                            media_type="text/plain")
        # TODO sprawdzić czy rezerwacja należy do usera

        if purchase_doc["payment_status"] != "pending":
            logger.info(f"Payment status for reservation {reservation_id} doesn't have pending status.")
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Reservation with ID {reservation_id} has already been paid for",
                            media_type="text/plain")

        reservation_creation_time = datetime.strptime(purchase_doc["reservation_creation_time"], "%Y-%m-%dT%H:%M:%S.%f")
        time_diff = (datetime.now() - reservation_creation_time).total_seconds()

        if time_diff > RESERVATION_EXPIRE_TIME:
            logger.info(f"Reservation {reservation_id} have expired by {time_diff - RESERVATION_EXPIRE_TIME} seconds.")
            payments_client = RabbitMQClient()
            payments_client.send_data_to_queue(queue_name=PURCHASES_PUBLISH_QUEUE_NAME,
                                               exchange_name=PURCHASES_EXCHANGE_NAME,
                                               payload=json.dumps({
                                                   "_id": reservation_id,
                                                   "payment_status": "expired",
                                               }, ensure_ascii=False).encode('utf-8'))
            payments_client.close_connection()

            MongoDBClient.payments_collection.update_one(filter={"_id": ObjectId(reservation_id)}, update={
                "$set": {"payment_status": "expired"}})

            return Response(status_code=status.HTTP_410_GONE,
                            content=f"Reservation with ID {reservation_id} has expired",
                            media_type="text/plain")

        if random.randint(1, 10) < CHANCE_OF_FAILING_PAYMENT:
            logger.info(f"Payment for reservation {reservation_id} was rejected.")
            payments_client = RabbitMQClient()
            payments_client.send_data_to_queue(queue_name=PURCHASES_PUBLISH_QUEUE_NAME,
                                               exchange_name=PURCHASES_EXCHANGE_NAME,
                                               payload=json.dumps({
                                                   "_id": reservation_id,
                                                   "payment_status": "rejected",
                                               }, ensure_ascii=False).encode('utf-8'))
            payments_client.close_connection()

            MongoDBClient.payments_collection.update_one(filter={"_id": ObjectId(reservation_id)}, update={
                "$set": {"payment_status": "rejected"}})

            return Response(status_code=status.HTTP_402_PAYMENT_REQUIRED,
                            content=f"Payment for reservation with ID {reservation_id} have failed",
                            media_type="text/plain")

        MongoDBClient.payments_collection.update_one(filter={"_id": ObjectId(reservation_id)}, update={
            "$set": {"payment_status": "accepted"}})

        payments_client = RabbitMQClient()
        payments_client.send_data_to_queue(queue_name=PURCHASES_PUBLISH_QUEUE_NAME,
                                           exchange_name=PURCHASES_EXCHANGE_NAME,
                                           payload=json.dumps({
                                               "_id": reservation_id,
                                               "payment_status": "accepted",
                                           }, ensure_ascii=False).encode('utf-8'))
        payments_client.close_connection()

        logger.info(f"Payment for reservation {reservation_id} was successfull.")
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"reservation_id": reservation_id, "receipt_id": "0987654321"},
                            media_type="application/json")

    except bson.errors.InvalidId:
        logger.info(f"Invalid reservation string")
        return Response(status_code=status.HTTP_404_NOT_FOUND,
                        content=f"Reservation with ID {reservation_id} does not exist",
                        media_type="text/plain")

    except Exception as ex:
        logger.info(f"Exception in payment ms occurred: {ex}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
