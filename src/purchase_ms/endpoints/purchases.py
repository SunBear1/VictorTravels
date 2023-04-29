import json
import logging

import bson.errors
from bson import ObjectId
from fastapi import APIRouter, status
from mongodb.mongodb_client import MongoDBClient
from rabbitmq.rabbitmq_client import RabbitMQClient, PAYMENTS_PUBLISH_QUEUE_NAME, PAYMENTS_EXCHANGE_NAME
from starlette.responses import JSONResponse, Response

router = APIRouter(prefix="/api/v1/purchase")

logger = logging.getLogger("purchases")


@router.post("/{reservation_id}",
             responses={
                 201: {"description": "Purchase performed successfully"},
                 200: {"description": "Purchase was already performed"},
                 404: {"description": "Reservation with provided ID does not exist"},
                 500: {"description": "Unknown error occurred"}
             },
             )
async def make_purchase(reservation_id: str):
    """
    Make a trip purchase by reservation
    """

    try:
        purchase_doc = MongoDBClient.purchases_collection.find_one({"_id": ObjectId(reservation_id)})
        if purchase_doc is None:
            logger.info(f"There is no information about the reservation")
            return Response(status_code=status.HTTP_404_NOT_FOUND,
                            content=f"Reservation with ID {reservation_id} does not exist",
                            media_type="text/plain")

        # TODO sprawdzić czy rezerwacja należy do usera

        if purchase_doc["purchase_status"] == "confirmed":
            logger.info(f"Purchase for reservation ID {reservation_id} was already done.")
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"reservation_id": reservation_id},
                                media_type="application/json")

        MongoDBClient.purchases_collection.update_one(filter={"_id": ObjectId(reservation_id)}, update={
            "$set": {"purchase_status": "confirmed"}})

        payments_client = RabbitMQClient()
        payments_client.send_data_to_queue(queue_name=PAYMENTS_PUBLISH_QUEUE_NAME, exchange_name=PAYMENTS_EXCHANGE_NAME,
                                           payload=json.dumps({
                                               "_id": reservation_id,
                                               "trip_offer_id": purchase_doc["trip_offer_id"],
                                               "purchase_status": "confirmed"
                                           }, ensure_ascii=False).encode('utf-8'))
        payments_client.close_connection()

        logger.info(f"Purchase for reservation ID {reservation_id} performed successfully.")
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"reservation_id": reservation_id},
                            media_type="application/json")
    except bson.errors.InvalidId:
        logger.info(f"Invalid reservation string")
        return Response(status_code=status.HTTP_404_NOT_FOUND,
                        content=f"Reservation with ID {reservation_id} does not exist",
                        media_type="text/plain")

    except Exception as ex:
        logger.info(f"Exception in purchase ms occurred: {ex}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
