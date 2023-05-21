import uuid

import requests
from fastapi import status


def test_register_user_success(gateway_users_url):
    example_user_login = f"{uuid.uuid4()}@victortravels.com"
    example_user_password = "my_very_safe_password"

    payload = {
        "email": example_user_login,
        "password": example_user_password
    }

    response = requests.post(f"{gateway_users_url}/register", json=payload, timeout=3)

    assert (response.status_code == status.HTTP_201_CREATED and
            response.text == f"Registered user with email: {example_user_login}")


def test_register_user_already_exists(gateway_users_url):
    example_user_login = f"{uuid.uuid4()}@victortravels.com"
    example_user_password = "my_very_safe_password"

    payload = {
        "email": example_user_login,
        "password": example_user_password
    }

    success_response = requests.post(f"{gateway_users_url}/register", json=payload)
    fail_response = requests.post(f"{gateway_users_url}/register", json=payload)

    assert (success_response.status_code == status.HTTP_201_CREATED and
            success_response.text == f"Registered user with email: {example_user_login}" and
            fail_response.status_code == status.HTTP_409_CONFLICT and
            fail_response.text == "User already exists")


def test_register_user_invalid_email(gateway_users_url):
    example_user_login = "123invalid-mail.com"
    example_user_password = "my_very_safe_password"

    payload = {
        "email": example_user_login,
        "password": example_user_password
    }
    response = requests.post(f"{gateway_users_url}/register", json=payload)

    assert (response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY and
            response.text == "User login is not a valid email address")


def test_login_user_success(gateway_users_url):
    example_user_login = f"{uuid.uuid4()}@victortravels.com"
    example_user_password = "my_very_safe_password"

    payload = {
        "email": example_user_login,
        "password": example_user_password
    }

    register_response = requests.post(f"{gateway_users_url}/register", json=payload)
    login_response = requests.post(f"{gateway_users_url}/login", json=payload)

    assert (register_response.status_code == status.HTTP_201_CREATED
            and register_response.text == f"Registered user with email: {example_user_login}"
            and login_response.status_code == status.HTTP_200_OK
            and login_response.text == f"Logged in user with email: {example_user_login}"
            and "Authorization" in login_response.headers
            and login_response.headers["Authorization"].startswith("Bearer ")
            )


def test_login_user_wrong_credentials(gateway_users_url):
    example_user_login = f"{uuid.uuid4()}@victortravels.com"
    example_user_password = "my_very_safe_password"
    wrong_example_user_password = "wrong_my_very_safe_password"

    register_payload = {
        "email": example_user_login,
        "password": example_user_password
    }

    login_payload = {
        "email": example_user_login,
        "password": wrong_example_user_password
    }

    register_response = requests.post(f"{gateway_users_url}/register", json=register_payload)
    login_response = requests.post(f"{gateway_users_url}/login", json=login_payload)

    assert (register_response.status_code == status.HTTP_201_CREATED
            and register_response.text == f"Registered user with email: {example_user_login}"
            and login_response.status_code == status.HTTP_401_UNAUTHORIZED
            and login_response.text == "User password or login does not match"
            and "Authorization" not in login_response.headers
            )


def test_login_user_not_exist(gateway_users_url):
    example_user_login = f"{uuid.uuid4()}@victortravels.com"
    example_user_password = "my_very_safe_password"

    payload = {
        "email": example_user_login,
        "password": example_user_password
    }

    login_response = requests.post(f"{gateway_users_url}/login", json=payload)

    assert (login_response.status_code == status.HTTP_401_UNAUTHORIZED
            and login_response.text == "User password or login does not match"
            and "Authorization" not in login_response.headers
            )
