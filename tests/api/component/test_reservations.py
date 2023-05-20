import json

import requests
from fastapi import status


def test_make_reservation_success(gateway_reservations_url, authorization_token):
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

    assert (response.status_code == status.HTTP_201_CREATED
            and "reservation_id" in json.loads(response.content.decode("utf-8")))


def test_make_reservation_insufficient_places(gateway_reservations_url, authorization_token):
    trip_offer_id = "0003"
    payload = {
        "hotel_id": "HFP-1",
        "room_type": "small",
        "connection_id_to": "KTK-RZE-PLANE-001",
        "connection_id_from": "RZE-KTK-TRAIN-001",
        "head_count": 1000000,
        "price": 2137.69
    }

    response = requests.post(f"{gateway_reservations_url}/{trip_offer_id}", json=payload,
                             headers={"Authorization": authorization_token})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # TODO add response.text assert


def test_make_reservation_not_found(gateway_reservations_url, authorization_token):
    trip_offer_id = "0000"
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

    assert response.status_code == status.HTTP_404_NOT_FOUND
    # TODO add response.text assert


def test_make_reservation_invalid_payload(gateway_reservations_url, authorization_token):
    trip_offer_id = "0000"
    payload = {
        "hotel_id": "HFP-1",
    }

    response = requests.post(f"{gateway_reservations_url}/{trip_offer_id}", json=payload,
                             headers={"Authorization": authorization_token})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_make_reservation_unauthorized(gateway_reservations_url):
    trip_offer_id = "0000"
    response = requests.post(f"{gateway_reservations_url}/{trip_offer_id}")

    assert (response.status_code == status.HTTP_401_UNAUTHORIZED
            and json.loads(response.content.decode("utf-8"))["detail"] == "Not authenticated")


def test_make_reservation_permission_denied(gateway_reservations_url):
    trip_offer_id = "0000"
    payload = {
        "hotel_id": "HFP-1",
        "room_type": "small",
        "connection_id_to": "KTK-RZE-PLANE-001",
        "connection_id_from": "RZE-KTK-TRAIN-001",
        "head_count": 1,
        "price": 2137.69
    }
    authorization_token = "Bearer IAMBADTOKEN"
    response = requests.post(f"{gateway_reservations_url}/{trip_offer_id}", json=payload,
                             headers={"Authorization": authorization_token})

    assert (response.status_code == status.HTTP_403_FORBIDDEN
            and response.text == "User does not have permission to use this service")
