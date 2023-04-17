import json
import logging
import sys

from db_clients import PostgreSQLClient, MongoDBClient, PG_DB_TRIPS_NAME, PG_DB_USERS_NAME

logger = logging.getLogger("data-init")

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.setLevel(logging.INFO)
logger.addHandler(handler)

if __name__ == "__main__":
    logger.info("Data initializer started")

    pg_client = PostgreSQLClient()
    pg_client.create_database(db_name=PG_DB_TRIPS_NAME)
    pg_client.create_database(db_name=PG_DB_USERS_NAME)
    pg_client.execute_query_for_database(db_name=PG_DB_USERS_NAME,
                                         query=open(file="postgresql_init_users.sql", mode="r",
                                                    encoding="utf-8").read())
    logger.info(f"Committed init {PG_DB_USERS_NAME} data to postgreSQL")
    pg_client.execute_query_for_database(db_name=PG_DB_TRIPS_NAME,
                                         query=open(file="postgresql_init_trips.sql", mode="r",
                                                    encoding="utf-8").read())

    logger.info(f"Committed init {PG_DB_TRIPS_NAME} data to postgreSQL")

    with open(file="mongo_init.json", mode="r", encoding="utf-8") as init_file:
        docs = json.load(init_file)

    try:
        MongoDBClient.trips_collection.insert_many(documents=docs)
    except Exception as ex:
        logger.info(f"Error occured when inserting data to mongodb: {ex}")

    logger.info("Committed init data to mongoDB")

    logger.info("Finished initializing data")
    sys.exit(0)
