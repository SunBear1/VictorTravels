import jwt
import psycopg2.errors

from common.authentication import hash_password, verify_password, JWT_SECRET, AUTHENTICATION_DISABLED
from sql.postgresql_client import PostgreSQLClient
from users.exceptions import UserAlreadyExistsException, UserNotExistException, UserWrongPasswordException
from users.models import UserUpdateData


def create_user(login: str, password: str):
    PostgreSQLClient.create_connection()

    try:
        PostgreSQLClient.client.execute(f"INSERT INTO users (login, password) VALUES (%(username)s, %(password)s);",
                                        {"username": login, "password": hash_password(password=password)})
        PostgreSQLClient.connection_to_database.commit()
        PostgreSQLClient.close_connection()

    except psycopg2.errors.UniqueViolation:
        PostgreSQLClient.close_connection()
        raise UserAlreadyExistsException(message="User already exists in database")


def get_user_by_login(login: str) -> dict[str: str]:
    PostgreSQLClient.create_connection()

    PostgreSQLClient.client.execute("SELECT id, login FROM users WHERE login=%(username)s;",
                                    {"username": login})
    query_result = PostgreSQLClient.client.fetchone()
    if query_result is None:
        raise UserNotExistException(message=f"User does not exist in database")
    user_data = {
        "id": query_result[0],
        "login": query_result[1],
    }

    PostgreSQLClient.close_connection()
    return user_data


def get_all_users() -> list[dict]:
    PostgreSQLClient.create_connection()

    PostgreSQLClient.client.execute("SELECT id, login FROM users;")
    query_result = list(PostgreSQLClient.client.fetchall())
    users_data = []
    for user in query_result:
        user_data = {
            "id": user[0],
            "login": user[1],
        }
        users_data.append(user_data)

    PostgreSQLClient.close_connection()
    return users_data


def delete_user_by_login(login: str):
    PostgreSQLClient.create_connection()

    PostgreSQLClient.client.execute("DELETE FROM users WHERE login=%(username)s;", {"username": login})

    query_result = PostgreSQLClient.client.fetchone()
    if query_result is None:
        raise UserNotExistException(message=f"User does not exist in database")
    else:
        PostgreSQLClient.connection_to_database.commit()

    PostgreSQLClient.close_connection()


def update_user_by_login(login: str, new_data: UserUpdateData):
    try:
        get_user_by_login(login=login)
    except UserNotExistException as ex:
        PostgreSQLClient.close_connection()
        raise ex

    PostgreSQLClient.create_connection()
    PostgreSQLClient.client.execute("UPDATE users SET login = %(new_login)s, password = %(password)s WHERE login=%("
                                    "login)s;",
                                    {"login": login, "new_login": new_data.email,
                                     "password": hash_password(password=new_data.password)})

    PostgreSQLClient.connection_to_database.commit()
    PostgreSQLClient.close_connection()


def authenticate_user(login: str, password: str) -> str:
    PostgreSQLClient.create_connection()
    PostgreSQLClient.client.execute("SELECT password FROM users WHERE login=%(username)s;",
                                    {"username": login})
    query_result = PostgreSQLClient.client.fetchone()
    if query_result is None:
        PostgreSQLClient.close_connection()
        raise UserNotExistException(message=f"User does not exist in database")
    if verify_password(password=password, hashed_password=query_result[0]):
        PostgreSQLClient.close_connection()
        return jwt.encode({"login": login, "password": password}, JWT_SECRET, algorithm='HS256')
    PostgreSQLClient.close_connection()
    raise UserWrongPasswordException(message=f"User password doesn't match")


def verify_user_identify(login: str, password: str) -> bool:
    if AUTHENTICATION_DISABLED:
        return True

    PostgreSQLClient.create_connection()
    PostgreSQLClient.client.execute("SELECT password FROM users WHERE login=%(username)s;",
                                    {"username": login})
    query_result = PostgreSQLClient.client.fetchone()
    if query_result is None:
        PostgreSQLClient.close_connection()
        return False
    if verify_password(password=password, hashed_password=query_result[0]):
        PostgreSQLClient.close_connection()
        return True
    PostgreSQLClient.close_connection()
    return False
