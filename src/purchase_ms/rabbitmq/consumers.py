import asyncio
import json
import logging
from bson import ObjectId

from mongodb.mongodb_client import MongoDBClient
from rabbitmq.rabbitmq_client import RabbitMQClient, PURCHASES_PUBLISH_QUEUE_NAME, PURCHASES_EXCHANGE_NAME

logger = logging.getLogger("purchases")


def start_consuming(queue_name, consume_function):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    consumer_client = RabbitMQClient()
    loop.run_until_complete(consumer_client.start_consuming(queue_name, consume_function))
    consumer_client.close_connection()


def consume_reservation_ms_event(ch, method, properties, body):
    received_msg = json.loads(body.decode('utf-8'))
    logger.info(msg=f"Received a message from Reservation MS: {received_msg}")
    init_document = {
        "_id": ObjectId(received_msg["_id"]),
        "trip_offer_id": received_msg["trip_offer_id"],
        "purchase_status": "pending",
        "payment_status": "pending",
        "uid": "example_uid",
        "price": received_msg["price"]
    }
    MongoDBClient.purchases_collection.insert_one(document=init_document)
    logger.info(f"Purchase entry for reservation {received_msg['_id']} successfully CREATED.")


def consume_payment_ms_event(ch, method, properties, body):
    received_msg = json.loads(body.decode('utf-8'))
    logger.info(msg=f"Received a message from Reservation MS: {received_msg}")
    MongoDBClient.purchases_collection.update_one(filter={"_id": ObjectId(received_msg["_id"])}, update={
        "$set": {"payment_status": received_msg["payment_status"]}})
    logger.info(f"Purchase entry for reservation {received_msg['_id']} UPDATED.")

    transaction_status = "canceled"
    if received_msg["payment_status"] == "accepted":
        transaction_status = "finalized"
    if received_msg["payment_status"] == "expired":
        transaction_status = "expired"

    purchases_client = RabbitMQClient()
    purchases_client.send_data_to_queue(queue_name=PURCHASES_PUBLISH_QUEUE_NAME, exchange_name=PURCHASES_EXCHANGE_NAME,
                                        payload=json.dumps({
                                            "_id": received_msg["_id"],
                                            "transaction_status": transaction_status,
                                        }, ensure_ascii=False).encode('utf-8'))
    purchases_client.close_connection()
