import uuid

import pytest
import requests


@pytest.fixture
def gateway_url():
    return "http://localhost:18000/api/v1/users"  # Replace with your base URL


def test_register_user_success(gateway_url):
    example_user_login = f"{uuid.uuid4()}@victortravels.com"
    example_user_password = "my_very_safe_password"

    payload = {
        "email": example_user_login,
        "password": example_user_password
    }

    response = requests.post(f"{gateway_url}/register", json=payload, timeout=3)

    assert (response.status_code == 201 and
            response.text == f"Registered user with email: {example_user_login}")


def test_register_user_already_exists(gateway_url):
    example_user_login = f"{uuid.uuid4()}@victortravels.com"
    example_user_password = "my_very_safe_password"

    payload = {
        "email": example_user_login,
        "password": example_user_password
    }

    success_response = requests.post(f"{gateway_url}/register", json=payload)
    fail_response = requests.post(f"{gateway_url}/register", json=payload)

    assert (success_response.status_code == 201 and
            success_response.text == f"Registered user with email: {example_user_login}" and
            fail_response.status_code == 409 and
            fail_response.text == "User already exists")


def test_register_user_invalid_email(gateway_url):
    example_user_login = "123invalid-mail.com"
    example_user_password = "my_very_safe_password"

    payload = {
        "email": example_user_login,
        "password": example_user_password
    }
    response = requests.post(f"{gateway_url}/register", json=payload)

    assert (response.status_code == 422 and
            response.text == "User login is not a valid email address")


def test_login_user_success(gateway_url):
    example_user_login = f"{uuid.uuid4()}@victortravels.com"
    example_user_password = "my_very_safe_password"

    payload = {
        "email": example_user_login,
        "password": example_user_password
    }

    register_response = requests.post(f"{gateway_url}/register", json=payload)
    login_response = requests.post(f"{gateway_url}/login", json=payload)

    assert (register_response.status_code == 201
            and register_response.text == f"Registered user with email: {example_user_login}"
            and login_response.status_code == 200
            and login_response.text == f"Logged in user with email: {example_user_login}"
            and "Authorization" in login_response.headers
            and login_response.headers["Authorization"].startswith("Bearer ")
            )
