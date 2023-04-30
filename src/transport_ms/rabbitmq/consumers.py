import asyncio
import json
import logging

from service.errors import UnprocessableEntityError
from service.transports_for_trip import get_offers_for_transport, check_if_transport_booked_up, \
    get_number_of_seats_left, update_left_seats_in_transport, get_transport_for_offer

from rabbitmq.rabbitmq_client import RabbitMQClient, TRIP_RESEARCHER_EXCHANGE_NAME, TRIP_RESEARCHER_PUBLISH_QUEUE_NAME, \
    EVENT_HUB_PUBLISH_QUEUE_NAME, EVENT_HUB_EXCHANGE_NAME

logger = logging.getLogger("transports")


def start_consuming(queue_name, consume_function):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    consumer_client = RabbitMQClient()
    loop.run_until_complete(consumer_client.start_consuming(queue_name, consume_function))
    consumer_client.close_connection()


def consume_eventhub_ms_event(ch, method, properties, body):
    received_msg = json.loads(body.decode('utf-8'))
    logger.info(msg=f"Received a message from EventHUB MS: {received_msg}")

    try:
        connection_id = get_transport_for_offer(trip_offer_id=received_msg["trip_offer_id"])
        logger.info(f"Connection ID of the offer {received_msg['trip_offer_id']} is {connection_id}.")

        if get_number_of_seats_left(connection_id=connection_id) == 0 and received_msg["operation_type"] == "delete":
            raise UnprocessableEntityError(f"There no more seats left in connection {connection_id}.")
    except UnprocessableEntityError as ex:
        logger.info(f"Exception occurred in TransportMS: {ex}")
        return

    offers = get_offers_for_transport(connection_id=connection_id)
    logger.info(f"Other trip offers for {connection_id} are {offers}.")

    transport_client = RabbitMQClient()
    transport_client.send_data_to_queue(queue_name=TRIP_RESEARCHER_PUBLISH_QUEUE_NAME,
                                        exchange_name=TRIP_RESEARCHER_EXCHANGE_NAME,
                                        payload=json.dumps({
                                            "title": "transport_update",
                                            "trip_offers_id": offers,
                                            "operation_type": received_msg["operation_type"],
                                            "connection_id": connection_id,
                                        }, ensure_ascii=False).encode('utf-8'))

    update_left_seats_in_transport(connection_id=connection_id,
                                   operation=received_msg["operation_type"])

    is_transport_booked_up = check_if_transport_booked_up(connection_id=connection_id)

    logger.info(msg=f"Transport {connection_id} booked up status: {is_transport_booked_up}")

    transport_booking_status_msg = {
        "title": "transport_booking_status",
        "trip_offers_id": offers,
        "connection_id": connection_id,
        "is_transport_booked_up": is_transport_booked_up,
    }

    transport_client.send_data_to_queue(queue_name=TRIP_RESEARCHER_PUBLISH_QUEUE_NAME,
                                        exchange_name=TRIP_RESEARCHER_EXCHANGE_NAME,
                                        payload=json.dumps(transport_booking_status_msg, ensure_ascii=False).encode(
                                            'utf-8'))

    transport_client.send_data_to_queue(queue_name=EVENT_HUB_PUBLISH_QUEUE_NAME,
                                        exchange_name=EVENT_HUB_EXCHANGE_NAME,
                                        payload=json.dumps(transport_booking_status_msg, ensure_ascii=False).encode(
                                            'utf-8'))
    transport_client.close_connection()
