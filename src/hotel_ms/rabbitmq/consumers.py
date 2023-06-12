import asyncio
import json
import logging

from service.hotels_for_trip import get_offers_for_hotel, get_hotel_for_offer, check_if_hotel_booked_up, \
    update_left_rooms_in_hotel, get_number_of_rooms_left

from rabbitmq.rabbitmq_client import RabbitMQClient, TRIP_RESEARCHER_EXCHANGE_NAME, TRIP_RESEARCHER_PUBLISH_QUEUE_NAME, \
    EVENT_HUB_PUBLISH_QUEUE_NAME, EVENT_HUB_EXCHANGE_NAME
from service.errors import UnprocessableEntityError

logger = logging.getLogger("hotels")


def start_consuming(queue_name, consume_function):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    consumer_client = RabbitMQClient()
    loop.run_until_complete(consumer_client.start_consuming(queue_name, consume_function))
    consumer_client.close_connection()


def consume_eventhub_ms_event(ch, method, properties, body):
    received_msg = json.loads(body.decode('utf-8'))
    logger.info(msg=f"Received a message from EventHUB MS: {received_msg}")
    if received_msg["resource_type"] == "price":
        handle_price_change_event(payload=received_msg)
    if received_msg["resource_type"] == "availability":
        handle_availability_change_event(payload=received_msg)


def handle_price_change_event(payload: dict):
    hotel_id = get_hotel_for_offer(trip_offer_id=payload["trip_offer_id"])
    offers = get_offers_for_hotel(hotel_id=hotel_id)

    hotels_client = RabbitMQClient()
    hotels_client.send_data_to_queue(queue_name=TRIP_RESEARCHER_PUBLISH_QUEUE_NAME,
                                     exchange_name=TRIP_RESEARCHER_EXCHANGE_NAME,
                                     payload=json.dumps({
                                         "title": "hotel_room_price_update",
                                         "trip_offers_id": offers,
                                         "operation_type": payload["operation_type"],
                                         "room_type": payload["room_type"],
                                         "resource_type": payload["resource_type"],
                                         "resource_amount": payload["resource_amount"]
                                     }, ensure_ascii=False).encode('utf-8'))
    hotels_client.close_connection()


def handle_availability_change_event(payload: dict):
    try:
        hotel_id = get_hotel_for_offer(trip_offer_id=payload["trip_offer_id"])
        if get_number_of_rooms_left(
                hotel_id=hotel_id,
                room_type=payload["room_type"]) - payload["resource_amount"] < 0 and payload[
            "operation_type"] == "delete":
            raise UnprocessableEntityError(f"There no more {payload['room_type']} rooms left in hotel {hotel_id}.")
    except UnprocessableEntityError as ex:
        logger.info(f"Exception occurred in HotelMS: {ex}")
        return

    offers = get_offers_for_hotel(hotel_id=hotel_id)

    hotels_client = RabbitMQClient()
    hotels_client.send_data_to_queue(queue_name=TRIP_RESEARCHER_PUBLISH_QUEUE_NAME,
                                     exchange_name=TRIP_RESEARCHER_EXCHANGE_NAME,
                                     payload=json.dumps({
                                         "title": "hotel_rooms_availability_update",
                                         "trip_offers_id": offers,
                                         "operation_type": payload["operation_type"],
                                         "room_type": payload["room_type"],
                                         "resource_type": payload["resource_type"],
                                         "resource_amount": payload["resource_amount"]
                                     }, ensure_ascii=False).encode('utf-8'))

    was_hotel_booked_up = check_if_hotel_booked_up(hotel_id=hotel_id)

    update_left_rooms_in_hotel(hotel_id=hotel_id, room_type=payload["room_type"],
                               operation=payload["operation_type"], rooms_amount=payload["resource_amount"])

    is_hotel_booked_up = check_if_hotel_booked_up(hotel_id=hotel_id)

    logger.info(msg=f"Hotel {hotel_id} booked up status: {is_hotel_booked_up}")

    hotel_booking_status_msg = {
        "title": "hotel_booking_status",
        "trip_offers_id": offers,
        "is_hotel_booked_up": is_hotel_booked_up,
    }

    if (was_hotel_booked_up and not is_hotel_booked_up) or (not was_hotel_booked_up and is_hotel_booked_up):
        hotels_client.send_data_to_queue(queue_name=TRIP_RESEARCHER_PUBLISH_QUEUE_NAME,
                                         exchange_name=TRIP_RESEARCHER_EXCHANGE_NAME,
                                         payload=json.dumps(hotel_booking_status_msg, ensure_ascii=False).encode(
                                             'utf-8'))

        hotels_client.send_data_to_queue(queue_name=EVENT_HUB_PUBLISH_QUEUE_NAME,
                                         exchange_name=EVENT_HUB_EXCHANGE_NAME,
                                         payload=json.dumps(hotel_booking_status_msg, ensure_ascii=False).encode(
                                             'utf-8'))
    hotels_client.close_connection()
