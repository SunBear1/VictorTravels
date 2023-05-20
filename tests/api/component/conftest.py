import json
import uuid

import pytest
import requests


@pytest.fixture
def gateway_reservations_url():
    return "http://localhost:18000/api/v1/reservations"


@pytest.fixture
def gateway_purchases_url():
    return "http://localhost:18000/api/v1/purchases"


@pytest.fixture
def gateway_payments_url():
    return "http://localhost:18000/api/v1/payments"


@pytest.fixture
def gateway_trips_url():
    return "http://localhost:18000/api/v1/trips"


@pytest.fixture
def gateway_users_url():
    return "http://localhost:18000/api/v1/users"


@pytest.fixture
def authorization_token(gateway_users_url) -> str:
    payload = {
        "email": f"{uuid.uuid4()}@victortravels.com",
        "password": "my_very_safe_password"
    }
    requests.post(f"{gateway_users_url}/register", json=payload)
    login_response = requests.post(f"{gateway_users_url}/login", json=payload)
    return login_response.headers["Authorization"]


@pytest.fixture
def reservation_id(gateway_reservations_url, gateway_users_url, authorization_token) -> str:
    payload = {
        "email": f"{uuid.uuid4()}@victortravels.com",
        "password": "my_very_safe_password"
    }
    requests.post(f"{gateway_users_url}/register", json=payload)
    requests.post(f"{gateway_users_url}/login", json=payload)

    trip_offer_id = "0003"
    payload = {
        "hotel_id": "HFP-1",
        "room_type": "small",
        "connection_id_to": "KTK-RZE-PLANE-001",
        "connection_id_from": "RZE-KTK-TRAIN-001",
        "head_count": 1,
        "price": 2137.69
    }

    response = requests.post(f"{gateway_reservations_url}/{trip_offer_id}", json=payload,
                             headers={"Authorization": authorization_token})

    return json.loads(response.content.decode("utf-8"))["reservation_id"]
