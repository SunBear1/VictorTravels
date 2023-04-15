import json
import logging

from db_clients import PostgreSQLClient, MongoDBClient, PG_DB_TRIPS_NAME, PG_DB_USERS_NAME

logger = logging.getLogger("gateway")

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
    # pg_client.execute_query_for_database(db_name=PG_DB_TRIPS_NAME,
    #                                      query=open(file="postgresql_init_trips.sql", mode="r",
    #                                                 encoding="utf-8").read())

    # pg_client.execute(f"CREATE DATABASE {PG_DB_TRIPS_NAME};")
    # PostgreSQLClient.connection_to_database.commit()
    # PostgreSQLClient.client.execute(f"CREATE DATABASE {PG_DB_USERS_NAME};")
    # PostgreSQLClient.connection_to_database.commit()
    # PostgreSQLClient.close_connection()
    # logger.info(f"Created databases {PG_DB_USERS_NAME} and {PG_DB_TRIPS_NAME}")
    #
    # PostgreSQLClient.create_connection(db_name=PG_DB_USERS_NAME)
    # PostgreSQLClient.client.execute(open(file="postgresql_init_users.sql", mode="r", encoding="utf-8").read())
    # PostgreSQLClient.connection_to_database.commit()
    # PostgreSQLClient.close_connection()
    # logger.info(f"Committed init {PG_DB_USERS_NAME} data to postgreSQL")
    #
    # PostgreSQLClient.create_connection(db_name=PG_DB_TRIPS_NAME)
    # PostgreSQLClient.client.execute(open(file="postgresql_init_trips.sql", mode="r", encoding="utf-8").read())
    # PostgreSQLClient.connection_to_database.commit()
    # PostgreSQLClient.close_connection()
    # logger.info(f"Committed init {PG_DB_TRIPS_NAME} data to postgreSQL")

    with open(file="mongo_init.json", mode="r", encoding="utf-8") as init_file:
        docs = json.load(init_file)

    for doc in docs:
        MongoDBClient.client.collection.insert_one(doc["trip"])
    logger.info("Committed init data to mongoDB")

    logger.info("Finished initializing data")
