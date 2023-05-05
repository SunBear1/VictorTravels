import logging

from mongodb.mongodb_client import MongoDBClient, HOTELS_DOCUMENT_ID, CONNECTIONS_DOCUMENT_ID

logger = logging.getLogger("reservations")


def check_if_hotel_exists(hotel_id: str) -> bool:
    hotels_document = MongoDBClient.trips_collection.find_one({"_id": HOTELS_DOCUMENT_ID})
    if hotel_id not in hotels_document:
        logger.info(f"There is no hotel with ID {hotel_id}.")
        return False
    return True


def check_if_connection_exists(connection_id: str) -> bool:
    connections_document = MongoDBClient.trips_collection.find_one({"_id": CONNECTIONS_DOCUMENT_ID})
    if connection_id not in connections_document:
        logger.info(f"There is no connection with ID {connection_id}.")
        return False
    return True


def check_if_rooms_available(hotel_id: str, room_type: str, rooms: int) -> bool:
    hotels_document = MongoDBClient.trips_collection.find_one({"_id": HOTELS_DOCUMENT_ID})
    if hotels_document[hotel_id][f"{room_type}roomsleft"] - rooms < 0:
        logger.info(f"Hotel {hotel_id} doesn't have any {room_type} rooms left.")
        return False
    return True


def check_if_connection_available(connection_id: str, seats: int) -> bool:
    connections_document = MongoDBClient.trips_collection.find_one({"_id": CONNECTIONS_DOCUMENT_ID})
    if connections_document[connection_id] - seats < 0:
        logger.info(f"Connection {connection_id} doesn't have enough seats left.")
        return False
    return True


def update_rooms_available(hotel_id: str, room_type: str, value: int):
    MongoDBClient.trips_collection.update_one(filter={"_id": HOTELS_DOCUMENT_ID}, update={
        "$inc": {f"{hotel_id}.{room_type}roomsleft": value}})
    logger.info(f"Room type {room_type} amount in hotel {hotel_id} changed by {value}.")


def update_seats_available(connection_id: str, value: int):
    MongoDBClient.trips_collection.update_one(filter={"_id": CONNECTIONS_DOCUMENT_ID}, update={
        "$inc": {f"{connection_id}": value}})
    logger.info(f"Seats amount in connection {connection_id} changed by {value}.")
