import logging
import os

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pymongo import MongoClient

PG_HOST = os.getenv("POSTGRES_ADDRESS", "localhost")
PG_USER = os.getenv("POSTGRES_USER", "admin")
PG_PASSWD = os.getenv("POSTGRES_PASSWORD", "admin")
PG_DB_TRIPS_NAME = os.getenv("POSTGRES_DB", "trips")
PG_DB_USERS_NAME = os.getenv("POSTGRES_DB", "users")
PG_PORT = os.getenv("POSTGRES_PORT", 5432)

MONGO_PORT = os.getenv("MONGODB_PORT", 27017)
MONGO_HOST = os.getenv("MONGODB_ADDRESS", "localhost")
MONGO_USER = os.getenv("MONGODB_USER", "admin")
MONGO_PASSWD = os.getenv("MONGODB_PASSWORD", "admin")
MONGO_DB_NAME = os.getenv("MONGODB_DB", "trips_db")
MONGO_COLLECTION_NAME = os.getenv("MONGODB_COLL", "trips")

logger = logging.getLogger("data-init")


class MongoDBClient:
    client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASSWD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin",
                         connectTimeoutMS=10000)
    db = client[MONGO_DB_NAME]
    trips_collection = db[MONGO_COLLECTION_NAME]


class PostgreSQLClient:
    def __init__(self):
        self.connection = None
        self.user = PG_USER
        self.password = PG_PASSWD
        self.host = PG_HOST
        self.port = PG_PORT

    def create_connection(self):
        # Connect to the PostgreSQL server without beginning a transaction block
        self.connection = psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            autocommit=True  # Set autocommit to True to disable transaction blocks
        )

    def execute_query_for_database(self, db_name: str, query: str):
        conn = psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=db_name
        )
        try:
            conn.cursor().execute(query)
            conn.commit()
        except Exception as ex:
            logger.info(f"Cant execute query because of: {ex}")
        finally:
            conn.close()

    def create_database(self, db_name: str):
        conn = psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )

        try:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            conn.cursor().execute(f"CREATE DATABASE {db_name};")
        except psycopg2.errors.DuplicateDatabase:
            logger.info(f"Database {db_name} already exists")
        finally:
            conn.close()
