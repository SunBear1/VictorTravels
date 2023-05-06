import json
import logging
import sys

from db_clients import PostgreSQLClient, MongoDBClient, PG_DB_USERS_NAME, \
    PG_DB_EVENTS_NAME, PG_DB_HOTELS_NAME, PG_DB_TRANSPORTS_NAME, MONGO_DB_TRIPS_NAME, MONGO_DB_RESERVATIONS_NAME

logger = logging.getLogger("data-init")

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.setLevel(logging.INFO)
logger.addHandler(handler)

if __name__ == "__main__":
    logger.info("Data initializer started")
    MongoDBClient.connect_to_database()

    postgres_init_data = [(PG_DB_USERS_NAME, "postgresql_init_users.sql"),
                          (PG_DB_EVENTS_NAME, "postgresql_init_events.sql"),
                          (PG_DB_HOTELS_NAME, "postgresql_init_hotels.sql"),
                          (PG_DB_TRANSPORTS_NAME, "postgresql_init_transports.sql"),
                          ]

    pg_client = PostgreSQLClient()
    for db_name, init_file in postgres_init_data:
        pg_client.create_database(db_name=db_name)
        pg_client.execute_query_for_database(db_name=db_name,
                                             query=open(file=init_file, mode="r",
                                                        encoding="utf-8").read())

    with open(file="mongodb_init_trips.json", mode="r", encoding="utf-8") as init_file:
        trips_db_docs = json.load(init_file)

    with open(file="mongodb_init_reservations.json", mode="r", encoding="utf-8") as init_file:
        reservation_db_docs = json.load(init_file)

    try:
        MongoDBClient.trips_collection.insert_many(documents=trips_db_docs)
        logger.info(f"Committed init {MONGO_DB_TRIPS_NAME} data to mongoDB")
        MongoDBClient.reservations_collection.insert_many(documents=reservation_db_docs)
        logger.info(f"Committed init {MONGO_DB_RESERVATIONS_NAME} data to mongoDB")
    except Exception as ex:
        logger.info(f"Error occurred when inserting data to mongodb: {ex}")

    logger.info("Finished initializing data")
    sys.exit(0)
