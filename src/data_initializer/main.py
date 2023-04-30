import json
import logging
import sys

from db_clients import PostgreSQLClient, MongoDBClient, PG_DB_USERS_NAME, MONGO_DB_NAME, \
    PG_DB_EVENTS_NAME, PG_DB_HOTELS_NAME

logger = logging.getLogger("data-init")

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.setLevel(logging.INFO)
logger.addHandler(handler)

if __name__ == "__main__":
    logger.info("Data initializer started")

    postgres_init_data = [(PG_DB_USERS_NAME, "postgresql_init_users.sql"),
                          (PG_DB_EVENTS_NAME, "postgresql_init_events.sql"),
                          (PG_DB_HOTELS_NAME, "postgresql_init_hotels.sql")
                          ]

    pg_client = PostgreSQLClient()
    for db_name, init_file in postgres_init_data:
        pg_client.create_database(db_name=db_name)
        pg_client.execute_query_for_database(db_name=db_name,
                                             query=open(file=init_file, mode="r",
                                                        encoding="utf-8").read())

    with open(file="mongo_init.json", mode="r", encoding="utf-8") as init_file:
        docs = json.load(init_file)

    try:
        MongoDBClient.trips_collection.insert_many(documents=docs)
    except Exception as ex:
        logger.info(f"Error occurred when inserting data to mongodb: {ex}")

    logger.info(f"Committed init {MONGO_DB_NAME} data to mongoDB")

    logger.info("Finished initializing data")
    sys.exit(0)
