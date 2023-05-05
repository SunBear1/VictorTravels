import asyncio
import json
import logging

from rabbitmq.rabbitmq_client import RabbitMQClient, TRIP_RESEARCHER_EXCHANGE_NAME, TRIP_RESEARCHER_PUBLISH_QUEUE_NAME, \
    EVENT_HUB_PUBLISH_QUEUE_NAME, EVENT_HUB_EXCHANGE_NAME
from service.errors import UnprocessableEntityError
from service.transports_for_trip import get_offers_for_transport, check_if_transport_booked_up, \
    get_number_of_seats_left, update_left_seats_in_transport

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
    connection_id = received_msg["connection_id"]
    operation_type = received_msg["operation_type"]
    head_count = received_msg["head_count"]

    try:
        if get_number_of_seats_left(connection_id=connection_id) - head_count < 0 and operation_type == "delete":
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
                                            "operation_type": operation_type,
                                            "connection_id": connection_id,
                                            "head_count": head_count
                                        }, ensure_ascii=False).encode('utf-8'))

    was_transport_booked_up = check_if_transport_booked_up(connection_id=connection_id)

    update_left_seats_in_transport(connection_id=connection_id,
                                   operation=operation_type, number_of_seats=head_count)

    is_transport_booked_up = check_if_transport_booked_up(connection_id=connection_id)

    logger.info(msg=f"Transport {connection_id} booked up status: {is_transport_booked_up}")

    transport_booking_status_msg = {
        "title": "transport_booking_status",
        "connection_id": connection_id,
        "trip_offers_id": [],
        "is_transport_booked_up": is_transport_booked_up,
    }

    if (was_transport_booked_up and not is_transport_booked_up) or (
            not was_transport_booked_up and is_transport_booked_up):
        transport_client.send_data_to_queue(queue_name=EVENT_HUB_PUBLISH_QUEUE_NAME,
                                            exchange_name=EVENT_HUB_EXCHANGE_NAME,
                                            payload=json.dumps(transport_booking_status_msg, ensure_ascii=False).encode(
                                                'utf-8'))

        transport_booking_status_msg["trip_offers_id"] = offers
        transport_client.send_data_to_queue(queue_name=TRIP_RESEARCHER_PUBLISH_QUEUE_NAME,
                                            exchange_name=TRIP_RESEARCHER_EXCHANGE_NAME,
                                            payload=json.dumps(transport_booking_status_msg, ensure_ascii=False).encode(
                                                'utf-8'))
    transport_client.close_connection()
