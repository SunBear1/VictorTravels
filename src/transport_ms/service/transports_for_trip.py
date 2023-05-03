import logging

from sql.postgresql_client import PostgreSQLClient

logger = logging.getLogger("transports")


def get_offers_for_transport(connection_id: str):
    trip_offer_id_query = f"SELECT TripOfferID FROM Offers WHERE ConnectionID = '{connection_id}';"

    pg_client = PostgreSQLClient()
    offers_query = pg_client.execute_query_for_database(query=trip_offer_id_query)

    return [offer[0] for offer in offers_query]


def update_left_seats_in_transport(connection_id: str, operation: str):
    math_operator = " - 1"
    if operation == "add":
        math_operator = " + 1"

    update_seats_query = f"UPDATE SeatsLeft SET seatsleft = seatsleft{math_operator} WHERE ConnectionID='{connection_id}';"

    pg_client = PostgreSQLClient()
    pg_client.execute_query_for_database(query=update_seats_query, fetch_data=False)


def check_if_transport_booked_up(connection_id: str) -> bool:
    check_transport_booked_up_query = f"SELECT ConnectionID FROM SeatsLeft WHERE ConnectionID='{connection_id}' AND seatsleft=0;"

    pg_client = PostgreSQLClient()
    transport_booked_up_query = pg_client.execute_query_for_database(query=check_transport_booked_up_query)

    result = True if transport_booked_up_query else False
    return result


def get_number_of_seats_left(connection_id: str) -> int:
    number_of_seats_left_query = f"SELECT SeatsLeft FROM SeatsLeft WHERE ConnectionID='{connection_id}';"

    pg_client = PostgreSQLClient()
    seats_left_query = pg_client.execute_query_for_database(query=number_of_seats_left_query)

    return seats_left_query[0][0]
