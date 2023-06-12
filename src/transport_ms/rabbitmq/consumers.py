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


def process_generated_event(payload: dict):
    connection_id = payload["connection_id"]
    operation_type = payload["operation_type"]

    transport_client = RabbitMQClient()
    connection_offers = get_offers_for_transport(connection_id=connection_id)

    if payload["resource_type"] == "availability":
        head_count = payload["value"]
        try:
            if get_number_of_seats_left(connection_id=connection_id) - head_count < 0 and operation_type == "delete":
                raise UnprocessableEntityError(f"There no more seats left in connection {connection_id}.")
        except UnprocessableEntityError as ex:
            logger.info(f"Exception occurred in TransportMS: {ex}")
            return

        logger.info(f"Other trip offers for {connection_id} are: {connection_offers}.")

        transport_client.send_data_to_queue(queue_name=TRIP_RESEARCHER_PUBLISH_QUEUE_NAME,
                                            exchange_name=TRIP_RESEARCHER_EXCHANGE_NAME,
                                            payload=json.dumps({
                                                "title": "generated_transport_availability_update",
                                                "trip_offers_id": connection_offers,
                                                "operation_type": operation_type,
                                                "connection_id": connection_id,
                                                "head_count": head_count
                                            }, ensure_ascii=False).encode('utf-8'))

        was_transport_booked_up = check_if_transport_booked_up(connection_id=connection_id)

        update_left_seats_in_transport(connection_id=connection_id,
                                       operation=operation_type, number_of_seats=head_count)

        is_transport_booked_up = check_if_transport_booked_up(connection_id=connection_id)

        transport_booking_status_msg = {
            "title": "transport_booking_status",
            "trip_offers_id": [],
        }

        send_booked_up_messages(rabbit_client=transport_client, was_transport_booked_up=was_transport_booked_up,
                                is_transport_booked_up=is_transport_booked_up,
                                msg_payload=transport_booking_status_msg,
                                offers=connection_offers, connection_id=connection_id)

    elif payload["resource_type"] == "price":
        transport_client.send_data_to_queue(queue_name=TRIP_RESEARCHER_PUBLISH_QUEUE_NAME,
                                            exchange_name=TRIP_RESEARCHER_EXCHANGE_NAME,
                                            payload=json.dumps({
                                                "title": "generated_transport_price_update",
                                                "trip_offers_id": connection_offers,
                                                "operation_type": operation_type,
                                                "connection_id": connection_id,
                                                "price": payload["value"]
                                            }, ensure_ascii=False).encode('utf-8'))

    transport_client.close_connection()


def process_reservation_event(payload: dict):
    connection_id_to = payload["connection_id_to"]
    connection_id_from = payload["connection_id_from"]
    operation_type = payload["operation_type"]
    head_count = payload["head_count"]

    try:
        if get_number_of_seats_left(connection_id=connection_id_to) - head_count < 0 and operation_type == "delete":
            raise UnprocessableEntityError(f"There no more seats left in connection {connection_id_to}.")
        if get_number_of_seats_left(connection_id=connection_id_from) - head_count < 0 and operation_type == "delete":
            raise UnprocessableEntityError(f"There no more seats left in connection {connection_id_from}.")
    except UnprocessableEntityError as ex:
        logger.info(f"Exception occurred in TransportMS: {ex}")
        return

    connection_to_offers = get_offers_for_transport(connection_id=connection_id_to)
    connection_from_offers = get_offers_for_transport(connection_id=connection_id_from)
    offers = list(set(connection_to_offers + connection_from_offers))
    logger.info(f"Other trip offers for {connection_id_to} and {connection_id_from} are: {offers}.")

    transport_client = RabbitMQClient()
    transport_client.send_data_to_queue(queue_name=TRIP_RESEARCHER_PUBLISH_QUEUE_NAME,
                                        exchange_name=TRIP_RESEARCHER_EXCHANGE_NAME,
                                        payload=json.dumps({
                                            "title": "transport_update",
                                            "trip_offers_id": offers,
                                            "operation_type": operation_type,
                                            "connection_id_to": connection_id_to,
                                            "connection_id_from": connection_id_from,
                                            "head_count": head_count
                                        }, ensure_ascii=False).encode('utf-8'))

    was_transport_to_booked_up = check_if_transport_booked_up(connection_id=connection_id_to)
    was_transport_from_booked_up = check_if_transport_booked_up(connection_id=connection_id_from)

    update_left_seats_in_transport(connection_id=connection_id_to,
                                   operation=operation_type, number_of_seats=head_count)
    update_left_seats_in_transport(connection_id=connection_id_from,
                                   operation=operation_type, number_of_seats=head_count)

    is_transport_to_booked_up = check_if_transport_booked_up(connection_id=connection_id_to)
    is_transport_from_booked_up = check_if_transport_booked_up(connection_id=connection_id_from)

    transport_booking_status_msg = {
        "title": "transport_booking_status",
        "trip_offers_id": [],
    }

    send_booked_up_messages(rabbit_client=transport_client, was_transport_booked_up=was_transport_to_booked_up,
                            is_transport_booked_up=is_transport_to_booked_up, msg_payload=transport_booking_status_msg,
                            offers=offers, connection_id=connection_id_to)
    send_booked_up_messages(rabbit_client=transport_client, was_transport_booked_up=was_transport_from_booked_up,
                            is_transport_booked_up=is_transport_from_booked_up,
                            msg_payload=transport_booking_status_msg,
                            offers=offers, connection_id=connection_id_from)

    transport_client.close_connection()


def consume_eventhub_ms_event(ch, method, properties, body):
    received_msg = json.loads(body.decode('utf-8'))
    logger.info(msg=f"Received a message from EventHUB MS: {received_msg}")
    if received_msg["title"] == "generated_transport_update":
        process_generated_event(payload=received_msg)
    if received_msg["title"] == "trip_offer_transport_update":
        process_reservation_event(payload=received_msg)


def send_booked_up_messages(rabbit_client: RabbitMQClient, was_transport_booked_up: bool, is_transport_booked_up: bool,
                            msg_payload: dict, offers: list, connection_id: str):
    message_payload = msg_payload.copy()
    if (was_transport_booked_up and not is_transport_booked_up) or (
            not was_transport_booked_up and is_transport_booked_up):
        message_payload["is_transport_booked_up"] = is_transport_booked_up
        message_payload["connection_id"] = connection_id
        rabbit_client.send_data_to_queue(queue_name=EVENT_HUB_PUBLISH_QUEUE_NAME,
                                         exchange_name=EVENT_HUB_EXCHANGE_NAME,
                                         payload=json.dumps(message_payload, ensure_ascii=False).encode(
                                             'utf-8'))

        message_payload["trip_offers_id"] = offers
        rabbit_client.send_data_to_queue(queue_name=TRIP_RESEARCHER_PUBLISH_QUEUE_NAME,
                                         exchange_name=TRIP_RESEARCHER_EXCHANGE_NAME,
                                         payload=json.dumps(message_payload, ensure_ascii=False).encode(
                                             'utf-8'))
