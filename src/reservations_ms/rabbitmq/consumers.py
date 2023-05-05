import asyncio
import json
import logging
from bson import ObjectId
from mongodb.mongodb_client import MongoDBClient, TRIP_OFFERS_DOCUMENT_ID, CONNECTIONS_DOCUMENT_ID
from service.trip_offers_handler import update_list_in_database

from rabbitmq.rabbitmq_client import RabbitMQClient, RESERVATIONS_PUBLISH_QUEUE_NAME, RESERVATIONS_EXCHANGE_NAME

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
    logger.info("Reservations entry for reservation successfully UPDATED.")

    if received_msg["transaction_status"] != "expired":
        reservation_doc = MongoDBClient.reservations_collection.find_one({"_id": ObjectId(received_msg["_id"])})
        reservations_client = RabbitMQClient()
        reservations_client.send_data_to_queue(queue_name=RESERVATIONS_PUBLISH_QUEUE_NAME,
                                               exchange_name=RESERVATIONS_EXCHANGE_NAME,
                                               payload=json.dumps({
                                                   "title": "reservation_status_update",
                                                   "trip_offer_id": reservation_doc["trip_offer_id"],
                                                   "reservation_id": received_msg["_id"],
                                                   "reservation_status": received_msg["transaction_status"],
                                               }, ensure_ascii=False).encode('utf-8'))
        reservations_client.close_connection()
        logger.info(f"Reservation {received_msg['_id']} ended with status {received_msg['transaction_status']}.")


def consume_eventhub_ms_event(ch, method, properties, body):
    received_msg = json.loads(body.decode('utf-8'))
    logger.info(msg=f"Received a message from EventHub MS: {received_msg}")

    if "trip_offers_affected" in received_msg and received_msg["trip_offers_affected"]:
        update_list_in_database(doc_id=TRIP_OFFERS_DOCUMENT_ID, key_in_doc="offers",
                                operation_type=received_msg["operation_type"],
                                received_values=received_msg["trip_offers_affected"])
    if "connection_affected" in received_msg and received_msg["connection_affected"]:
        update_list_in_database(doc_id=CONNECTIONS_DOCUMENT_ID, key_in_doc="connections",
                                operation_type=received_msg["operation_type"],
                                received_values=received_msg["connection_affected"])
