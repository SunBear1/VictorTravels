import logging
import os
import psycopg2
from typing import List

PG_HOST = os.getenv("POSTGRES_ADDRESS", "localhost")
PG_USER = os.getenv("POSTGRES_USER", "admin")
PG_PASSWD = os.getenv("POSTGRES_PASSWORD", "admin")
PG_DB_HOTELS_NAME = os.getenv("PG_DB_HOTELS_NAME", "hotels")
PG_PORT = os.getenv("POSTGRES_PORT", 5432)

logger = logging.getLogger("hotels")


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
        )

    def execute_query_for_database(self, query: str, db_name: str = PG_DB_HOTELS_NAME, fetch_data: bool = True) -> List:
        conn = psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=db_name
        )
        cursor = conn.cursor()
        try:
            cursor.execute(query=query)
            conn.commit()
            logger.info(f"Executed query {query} to {db_name} database.")
            if fetch_data:
                query_result = cursor.fetchall()
                return query_result
        except Exception as ex:
            logger.info(f"Cant execute query because of: {ex}")
            raise ex
        finally:
            cursor.close()
            conn.close()
