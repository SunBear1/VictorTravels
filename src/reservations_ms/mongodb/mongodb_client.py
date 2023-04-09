from pymongo import MongoClient

DB_ADDRESS = "mongodb://admin:admin@localhost:27017/?authSource=admin"
DB_NAME = "reservations_db"
TRIPS_COLLECTION_NAME = "trips"
RESERVATIONS_COLLECTION_NAME = "reservations"


class MongoDBClient:
    client = MongoClient(DB_ADDRESS)
    db = client[DB_NAME]
    trips_collection = db[TRIPS_COLLECTION_NAME]
    reservations_collection = db[RESERVATIONS_COLLECTION_NAME]
