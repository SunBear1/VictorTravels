import logging

from mongodb.mongodb_client import MongoDBClient, TRIP_OFFERS_DOCUMENT_ID, CONNECTIONS_DOCUMENT_ID

logger = logging.getLogger("reservations")


def check_if_trip_offer_exists(trip_offer_id: str) -> bool:
    trips_document = MongoDBClient.trips_collection.find_one({"_id": TRIP_OFFERS_DOCUMENT_ID})
    if trip_offer_id not in trips_document["offers"]:
        logger.info(f"From available trip offers {trips_document['offers']} there is no value {trip_offer_id}.")
        return False
    return True


def check_if_connection_exists(connection_id: str) -> bool:
    connections_document = MongoDBClient.trips_collection.find_one({"_id": CONNECTIONS_DOCUMENT_ID})
    if connection_id not in connections_document["connections"]:
        logger.info(
            f"From available connections {connections_document['connections']} there is no value {connection_id}.")
        return False
    return True


def update_list_in_database(doc_id: str, key_in_doc: str, operation_type: str, received_values: list):
    if operation_type == "add":
        MongoDBClient.trips_collection.update_one(
            filter={"_id": doc_id},
            update={"$addToSet": {key_in_doc: {"$each": received_values}}},
        )
        logger.info(f"New {received_values} ADDED to {doc_id}.")
    elif operation_type == "delete":
        MongoDBClient.trips_collection.update_one(
            filter={"_id": doc_id},
            update={"$pull": {key_in_doc: {"$in": received_values}}}
        )
        logger.info(f"New {received_values} DELETED from {doc_id}.")
