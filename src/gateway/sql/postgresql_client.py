import os

import psycopg2

HOST = os.getenv("POSTGRES_ADDRESS", "localhost")
USER = os.getenv("POSTGRES_USER", "admin")
PASSWD = os.getenv("POSTGRES_PASSWORD", "admin")
DB_NAME = os.getenv("POSTGRES_DB", "users")
PORT = os.getenv("POSTGRES_PORT", 5432)


class PostgreSQLClient:
    connection_to_database = None
    client = None

    @classmethod
    def create_connection(cls):
        cls.connection_to_database = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWD,
            database=DB_NAME,
            port=PORT,
        )
        cls.client = cls.connection_to_database.cursor()

    @classmethod
    def close_connection(cls):
        cls.client.close()
        cls.connection_to_database.close()
