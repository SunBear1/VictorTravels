import logging
import os

from pymongo import MongoClient

PORT = os.getenv("MONGODB_PORT", 27017)
HOST = os.getenv("MONGODB_ADDRESS", "localhost")
USER = os.getenv("MONGODB_USER", "admin")
PASSWD = os.getenv("MONGODB_PASSWORD", "admin")
DB_NAME = os.getenv("MONGODB_DB", "reservations_db")

TRIPS_COLLECTION_NAME = "trip-offers"
RESERVATIONS_COLLECTION_NAME = "reservations"
TRIP_OFFERS_DOCUMENT_ID = "available_trip_offers"
CONNECTIONS_DOCUMENT_ID = "available_connections"

logger = logging.getLogger("reservations")


class MongoDBClient:
    client = MongoClient(f"mongodb://{USER}:{PASSWD}@{HOST}:{PORT}/?authSource=admin", connectTimeoutMS=10000)
    db = client[DB_NAME]
    trips_collection = db[TRIPS_COLLECTION_NAME]
    reservations_collection = db[RESERVATIONS_COLLECTION_NAME]
    logger.info(f"Connection to mongoDB at {HOST}:{PORT} established.")
