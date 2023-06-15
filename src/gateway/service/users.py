import jwt
import psycopg2.errors

from common.authentication import verify_password, JWT_SECRET, AUTHENTICATION_DISABLED, hash_password
from sql.postgresql_client import PostgreSQLClient
from users.exceptions import UserAlreadyExistsException, UserNotExistException, UserWrongPasswordException
from users.models import UserUpdateData


def create_user(login: str, password: str):
    pg_client = PostgreSQLClient()

    hashed_password = hash_password(password=password)
    try:
        create_user_query = pg_client.execute_query_for_database(
            query=f"INSERT INTO users (login, password) VALUES ('{login}', '{hashed_password}');", fetch_data=False)

    except psycopg2.errors.UniqueViolation:
        raise UserAlreadyExistsException(message="User already exists in database")


def get_user_by_login(login: str) -> dict[str: str]:
    pg_client = PostgreSQLClient()
    query_result = pg_client.execute_query_for_database(
        query=f"SELECT id, login FROM users WHERE login = '{login}';"
    )
    if not query_result:
        raise UserNotExistException(message="User does not exist in the database.")

    user_data = {
        "id": query_result[0][0],
        "login": query_result[0][1]
    }
    return user_data


def get_all_users() -> list[dict]:
    pg_client = PostgreSQLClient()
    query_result = pg_client.execute_query_for_database(query="SELECT id, login FROM users;")
    users_data = []
    for user in query_result:
        user_data = {
            "id": user[0],
            "login": user[1]
        }
        users_data.append(user_data)
    return users_data


def delete_user_by_login(login: str):
    pg_client = PostgreSQLClient()
    pg_client.execute_query_for_database(query=f"DELETE FROM users WHERE login = '{login}';", fetch_data=False)
    if not pg_client.rowcount:
        raise UserNotExistException(message="User does not exist in the database.")


def update_user_by_login(login: str, new_data: UserUpdateData):
    try:
        get_user_by_login(login=login)
    except UserNotExistException as ex:
        raise ex

    pg_client = PostgreSQLClient()
    pg_client.execute_query_for_database(
        query=f"UPDATE users SET login = '{new_data.email}', password = '{new_data.password}' WHERE login = '{login}';"
    )


def authenticate_user(login: str, password: str) -> str:
    pg_client = PostgreSQLClient()
    query_result = pg_client.execute_query_for_database(
        query=f"SELECT password FROM users WHERE login = '{login}';"
    )
    if not query_result:
        raise UserNotExistException(message="User does not exist in the database.")

    if verify_password(password=password, hashed_password=query_result[0][0]):
        return jwt.encode({"login": login, "password": password}, JWT_SECRET, algorithm='HS256')

    raise UserWrongPasswordException(message="User password doesn't match")


def verify_user_identify(login: str, password: str) -> bool:
    if AUTHENTICATION_DISABLED:
        return True

    pg_client = PostgreSQLClient()
    query_result = pg_client.execute_query_for_database(
        query=f"SELECT password FROM users WHERE login = '{login}';"
    )
    if not query_result:
        return False

    if verify_password(password=password, hashed_password=query_result[0][0]):
        return True

    return False
