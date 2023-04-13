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


@router.post("/{reservation_id}",
             responses={
                 201: {"description": "Payment performed successfully"},
                 404: {"description": "Reservation with provided ID does not exist"},
                 400: {"description": "Reservation with provided ID has already been paid for"},
                 410: {"description": "Reservation with ID has expired"},
                 402: {"description": "Payment for reservation with ID have failed"},
                 500: {"description": "Unknown error occurred"}
             },
             )
async def make_payment(reservation_id: str):
    """
    Make a trip purchase by reservation
    """

    try:
        current_time = datetime.now()
        purchase_doc = MongoDBClient.payments_collection.find_one({"_id": ObjectId(reservation_id)})
        if "purchase_status" not in purchase_doc:
            logger.info(f"There is no information about the reservation purchase")
            return Response(status_code=status.HTTP_404_NOT_FOUND,
                            content=f"Reservation with ID {reservation_id} has not been purchased",
                            media_type="text/plain")

        # TODO sprawdzić czy rezerwacja należy do usera

        if purchase_doc["payment_status"] != "pending":
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Reservation with ID {reservation_id} has already been paid for",
                            media_type="text/plain")

        reservation_creation_time = datetime.strptime(purchase_doc["reservation_creation_time"], "%Y-%m-%d:%H:%M:%S")
        time_diff = (current_time - reservation_creation_time).total_seconds()

        if time_diff > 180:
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

        if random.randint(1, 10) > 7:
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
