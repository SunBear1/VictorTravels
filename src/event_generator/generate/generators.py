import random
from typing import Dict

from data.connections import CONNECTIONS_REGISTRY
from data.hotels import HOTELS_REGISTRY

MSG_TITLE = "generated_offer_change_live_event"


def generate_hotel_price_change() -> Dict:
    random_hotel = random.choice(list(HOTELS_REGISTRY.keys()))
    random_room = random.choice(list(HOTELS_REGISTRY[random_hotel].keys()))
    random_price_change = random.randrange(start=20, stop=55, step=5)

    return {
        "title": MSG_TITLE,
        "type": "hotel",
        "name": random_hotel,
        "field": random_room,
        "resource": "price",
        "value": random_price_change,
        "operation": random.choice(["add", "delete"])
    }


def generate_connection_price_change() -> Dict:
    random_connection = random.choice(list(CONNECTIONS_REGISTRY.keys()))
    random_price_change = random.randrange(start=10, stop=35, step=5)

    return {
        "title": MSG_TITLE,
        "type": "connection",
        "name": random_connection,
        "field": None,
        "resource": "price",
        "value": random_price_change,
        "operation": random.choice(["add", "delete"])
    }


def generate_hotel_availability_change() -> Dict:
    random_hotel = random.choice(list(HOTELS_REGISTRY.keys()))
    random_room = random.choice(list(HOTELS_REGISTRY[random_hotel].keys()))
    current_rooms_left = HOTELS_REGISTRY[random_hotel][random_room]

    random_rooms_left_change = random.randint(a=1, b=3)
    if current_rooms_left - random_rooms_left_change < 0:
        operation = "add"
    else:
        operation = random.choice(["add", "delete"])

    return {
        "title": MSG_TITLE,
        "type": "hotel",
        "name": random_hotel,
        "field": random_room,
        "resource": "availability",
        "value": random_rooms_left_change,
        "operation": operation
    }


def generate_connection_availability_change() -> Dict:
    random_connection = random.choice(list(CONNECTIONS_REGISTRY.keys()))
    current_seats_left = CONNECTIONS_REGISTRY[random_connection]

    random_seats_left_change = random.randint(a=1, b=6)
    if current_seats_left - random_seats_left_change < 0:
        operation = "add"
    else:
        operation = random.choice(["add", "delete"])

    return {
        "title": MSG_TITLE,
        "type": "connection",
        "name": random_connection,
        "field": None,
        "resource": "availability",
        "value": random_seats_left_change,
        "operation": operation
    }
