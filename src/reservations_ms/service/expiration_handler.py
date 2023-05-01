import asyncio
import json
import logging

from bson import ObjectId

from mongodb.mongodb_client import MongoDBClient
from rabbitmq.rabbitmq_client import RabbitMQClient, RESERVATIONS_PUBLISH_QUEUE_NAME, RESERVATIONS_EXCHANGE_NAME

logger = logging.getLogger("reservations")

RESERVATION_EXPIRE_TIME = 180


async def start_measuring_reservation_time(reservation_id: str, reservation_creation_time: str):
    logger.info(f"Reservation {reservation_id} created at {reservation_creation_time}. Expiration timer started.")
    await asyncio.sleep(delay=RESERVATION_EXPIRE_TIME)
    reservation_doc = MongoDBClient.reservations_collection.find_one({"_id": ObjectId(reservation_id)})
    if reservation_doc["reservation_status"] == "temporary":
        logger.info(f"Reservation {reservation_id} expired. Sending message to EventHub MS.")
        MongoDBClient.reservations_collection.update_one(filter={"_id": ObjectId(reservation_id)}, update={
            "$set": {"reservation_status": "expired"}})
        reservations_client = RabbitMQClient()
        reservations_client.send_data_to_queue(queue_name=RESERVATIONS_PUBLISH_QUEUE_NAME,
                                               exchange_name=RESERVATIONS_EXCHANGE_NAME,
                                               payload=json.dumps({
                                                   "trip_offer_id": reservation_doc["trip_offer_id"],
                                                   "reservation_id": reservation_id,
                                                   "reservation_status": "expired",
                                               }, ensure_ascii=False).encode('utf-8'))
        reservations_client.close_connection()
