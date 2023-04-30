import asyncio
import json
import logging

from service.errors import UnprocessableEntityError
from service.hotels_for_trip import get_offers_for_hotel, get_hotel_for_offer, check_if_hotel_booked_up, \
    update_left_rooms_in_hotel, get_number_of_rooms_left

from rabbitmq.rabbitmq_client import RabbitMQClient, TRIP_RESEARCHER_EXCHANGE_NAME, TRIP_RESEARCHER_PUBLISH_QUEUE_NAME, \
    EVENT_HUB_PUBLISH_QUEUE_NAME, EVENT_HUB_EXCHANGE_NAME

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

    try:
        hotel_id = get_hotel_for_offer(trip_offer_id=received_msg["trip_offer_id"])
        logger.info(f"Hotel ID of the offer {received_msg['trip_offer_id']} is {hotel_id}.")
        if get_number_of_rooms_left(
                hotel_id=hotel_id,
                room_type=received_msg["room_type"]) == 0 and received_msg["operation_type"] == "delete":
            raise UnprocessableEntityError(f"There no more {received_msg['room_type']} rooms left in hotel {hotel_id}.")
    except UnprocessableEntityError as ex:
        logger.info(f"Exception occurred in HotelMS: {ex}")
        return

    offers = get_offers_for_hotel(hotel_id=hotel_id)
    logger.info(f"Other trip offers for {hotel_id} are {offers}.")

    hotels_client = RabbitMQClient()
    hotels_client.send_data_to_queue(queue_name=TRIP_RESEARCHER_PUBLISH_QUEUE_NAME,
                                     exchange_name=TRIP_RESEARCHER_EXCHANGE_NAME,
                                     payload=json.dumps({
                                         "title": "hotel_rooms_update",
                                         "trip_offers_id": offers,
                                         "operation_type": received_msg["operation_type"],
                                         "room_type": received_msg["room_type"],
                                     }, ensure_ascii=False).encode('utf-8'))

    update_left_rooms_in_hotel(hotel_id=hotel_id, room_type=received_msg["room_type"],
                               operation=received_msg["operation_type"])

    is_hotel_booked_up = check_if_hotel_booked_up(hotel_id=hotel_id)

    logger.info(msg=f"Hotel {hotel_id} booked up status: {is_hotel_booked_up}")

    hotel_booking_status_msg = {
        "title": "hotel_booking_status",
        "trip_offers_id": offers,
        "is_hotel_booked_up": is_hotel_booked_up,
    }

    hotels_client.send_data_to_queue(queue_name=TRIP_RESEARCHER_PUBLISH_QUEUE_NAME,
                                     exchange_name=TRIP_RESEARCHER_EXCHANGE_NAME,
                                     payload=json.dumps(hotel_booking_status_msg, ensure_ascii=False).encode('utf-8'))

    hotels_client.send_data_to_queue(queue_name=EVENT_HUB_PUBLISH_QUEUE_NAME,
                                     exchange_name=EVENT_HUB_EXCHANGE_NAME,
                                     payload=json.dumps(hotel_booking_status_msg, ensure_ascii=False).encode('utf-8'))
    hotels_client.close_connection()
