import logging
import os

from pymongo import MongoClient

PORT = os.getenv("MONGODB_PORT", 27017)
HOST = os.getenv("MONGODB_ADDRESS", "localhost")
USER = os.getenv("MONGODB_USER", "admin")
PASSWD = os.getenv("MONGODB_PASSWORD", "admin")
DB_NAME = os.getenv("MONGODB_DB", "payments_db")

PURCHASES_COLLECTION_NAME = "purchases"

logger = logging.getLogger("purchases")


class MongoDBClient:
    client = MongoClient(f"mongodb://{USER}:{PASSWD}@{HOST}:{PORT}/?authSource=admin", connectTimeoutMS=10000)
    db = client[DB_NAME]
    purchases_collection = db[PURCHASES_COLLECTION_NAME]
    logger.info(f"Connection to mongoDB at {HOST}:{PORT} established.")
