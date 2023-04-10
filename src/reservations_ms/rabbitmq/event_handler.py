import asyncio
import json

from bson import ObjectId

from mongodb.mongodb_client import MongoDBClient
from rabbitmq.rabbitmq_client import RabbitMQClient


def start_consuming(queue_name, consume_function):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = RabbitMQClient.get_instance()
    loop.run_until_complete(client.start_consuming(queue_name, consume_function))


def consume_purchase_ms_event(ch, method, properties, body):
    received_msg = json.loads(body.decode('utf-8'))
    print(f"WOW I GOT: {received_msg} FROM PURCHASE MS")
    MongoDBClient.reservations_collection.update_one(filter={"_id": ObjectId(received_msg["_id"])}, update={
        "$set": {"reservation_status": received_msg["transaction_status"]}})
    print(MongoDBClient.reservations_collection.find_one(filter={"_id": ObjectId(received_msg["_id"])}))


def consume_director_ms_event(ch, method, properties, body):
    received_msg = json.loads(body.decode('utf-8'))
    trips_document_id = "trips-list"
    print(f"WOW I GOT: {received_msg} FROM DIRECTOR MS")
    if received_msg["operation_type"] == "Add":
        MongoDBClient.trips_collection.update_one(
            filter={"_id": trips_document_id},
            update={"$addToSet": {"trips": {"$each": received_msg["trips_affected"]}}},
            upsert=True
        )
    elif received_msg["operation_type"] == "Delete":
        MongoDBClient.trips_collection.update_one(
            {"_id": trips_document_id},
            {"$pull": {"trips": {"$in": received_msg["trips_affected"]}}}
        )
    else:
        print("Invalid operation type:", received_msg["operation_type"])
