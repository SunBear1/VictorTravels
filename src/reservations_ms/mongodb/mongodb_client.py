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
HOTELS_DOCUMENT_ID = "available_hotels"
CONNECTIONS_DOCUMENT_ID = "available_connections"

logger = logging.getLogger("reservations")


class MongoDBClient:
    client = MongoClient(f"mongodb://{USER}:{PASSWD}@{HOST}:{PORT}", connectTimeoutMS=10000)
    db = client[DB_NAME]
    trips_collection = db[TRIPS_COLLECTION_NAME]
    reservations_collection = db[RESERVATIONS_COLLECTION_NAME]

    @classmethod
    def connect_to_database(cls):
        try:
            cls.db.command('ping')
            logger.info(
                f"Connection to mongoDB at {HOST}:{PORT} as user {USER} for DB {DB_NAME} established.")
        except Exception as e:
            logger.info("Unable to connect to MongoDB:", e)
