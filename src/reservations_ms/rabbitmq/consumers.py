import asyncio
import json
import logging

from bson import ObjectId
from mongodb.mongodb_client import MongoDBClient, TRIPS_DOCUMENT_ID

from rabbitmq.rabbitmq_client import RabbitMQClient

logger = logging.getLogger("reservations")


def start_consuming(queue_name, consume_function):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    consumer_client = RabbitMQClient()
    loop.run_until_complete(consumer_client.start_consuming(queue_name, consume_function))
    consumer_client.close_connection()


def consume_purchase_ms_event(ch, method, properties, body):
    received_msg = json.loads(body.decode('utf-8'))
    logger.info(msg=f"Received a message from Purchase MS: {received_msg}")
    MongoDBClient.reservations_collection.update_one(filter={"_id": ObjectId(received_msg["_id"])}, update={
        "$set": {"reservation_status": received_msg["transaction_status"]}})


def consume_director_ms_event(ch, method, properties, body):
    received_msg = json.loads(body.decode('utf-8'))
    logger.info(msg=f"Received a message from Director MS: {received_msg}")
    if received_msg["operation_type"] == "Add":
        MongoDBClient.trips_collection.update_one(
            filter={"_id": TRIPS_DOCUMENT_ID},
            update={"$addToSet": {"trips": {"$each": received_msg["trips_affected"]}}},
            upsert=True
        )
    elif received_msg["operation_type"] == "Delete":
        MongoDBClient.trips_collection.update_one(
            {"_id": TRIPS_DOCUMENT_ID},
            {"$pull": {"trips": {"$in": received_msg["trips_affected"]}}}
        )
    else:
        print("Invalid operation type:", received_msg["operation_type"])
