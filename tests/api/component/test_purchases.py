import json
from time import sleep

import requests
from fastapi import status


def test_purchase_trip_reservation_not_found(gateway_purchases_url, authorization_token):
    response = requests.post(f"{gateway_purchases_url}/123",
                             headers={"Authorization": authorization_token})

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_purchase_trip_unauthorized(gateway_purchases_url):
    response = requests.post(f"{gateway_purchases_url}/1234")

    assert (response.status_code == status.HTTP_401_UNAUTHORIZED
            and json.loads(response.content.decode("utf-8"))["detail"] == "Not authenticated")


def test_purchase_trip_permission_denied(gateway_purchases_url):
    authorization_token = "Bearer IAMBADTOKEN"
    response = requests.post(f"{gateway_purchases_url}/1234", headers={"Authorization": authorization_token})

    assert (response.status_code == status.HTTP_403_FORBIDDEN
            and response.text == "User does not have permission to use this service")


def test_purchase_trip_success(gateway_purchases_url, reservation_id, authorization_token):
    sleep(0.1)  # PyTest is faster then RabbitMQ
    response = requests.post(f"{gateway_purchases_url}/{reservation_id}",
                             headers={"Authorization": authorization_token})

    assert (response.status_code == status.HTTP_201_CREATED
            and "reservation_id" in json.loads(response.content.decode("utf-8")))
