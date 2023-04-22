import asyncio
import json
import logging

from bson import ObjectId

from mongodb.mongodb_client import MongoDBClient
from rabbitmq.rabbitmq_client import RabbitMQClient

logger = logging.getLogger("payments")


def start_consuming(queue_name, consume_function):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    consumer_client = RabbitMQClient()
    loop.run_until_complete(consumer_client.start_consuming(queue_name, consume_function))
    consumer_client.close_connection()


def consume_purchase_ms_event(ch, method, properties, body):
    received_msg = json.loads(body.decode('utf-8'))
    if "reservation_creation_time" in received_msg:
        logger.info(msg=f"Received a message from reservation MS: {received_msg}")
        init_document = {
            "_id": ObjectId(received_msg["_id"]),
            "reservation_creation_time": received_msg["reservation_creation_time"],
            "purchase_status": "pending",
            "payment_status": "pending",
            "uid": "example_uid"
        }
        MongoDBClient.payments_collection.insert_one(document=init_document)
    else:
        logger.info(msg=f"Received a message from purchase MS: {received_msg}")
        MongoDBClient.payments_collection.update_one(filter={"_id": ObjectId(received_msg["_id"])}, update={
            "$set": {
                "trip_id": received_msg["trip_id"],
                "purchase_status": received_msg["purchase_status"]
            }}, upsert=True)
