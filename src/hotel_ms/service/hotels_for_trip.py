import logging

from sql.postgresql_client import PostgreSQLClient

logger = logging.getLogger("hotels")


def get_hotel_for_offer(trip_offer_id: str) -> str:
    hotel_id_query = f"SELECT HotelID FROM Offers WHERE TripOfferID='{trip_offer_id}';"

    pg_client = PostgreSQLClient()
    hotel_query = pg_client.execute_query_for_database(query=hotel_id_query)

    return hotel_query[0][0]


def get_offers_for_hotel(hotel_id: str):
    trip_offer_id_query = f"SELECT TripOfferID FROM Offers WHERE HotelID='{hotel_id}';"

    pg_client = PostgreSQLClient()
    offers_query = pg_client.execute_query_for_database(query=trip_offer_id_query)

    return [offer[0] for offer in offers_query]


def update_left_rooms_in_hotel(hotel_id: str, room_type: str):
    update_rooms_query = f"UPDATE Offers SET {room_type}roomsleft = {room_type}roomsleft - 1, WHERE HotelID='{hotel_id}';"

    pg_client = PostgreSQLClient()
    rooms_query = pg_client.execute_query_for_database(query=update_rooms_query)

    return rooms_query


def check_if_hotel_booked_up(hotel_id: str) -> bool:
    ...
