import json
from time import sleep

import requests
from fastapi import status


def test_payment_for_trip_reservation_not_found(gateway_payments_url, authorization_token):
    non_existing_reservation_id = 123
    response = requests.post(f"{gateway_payments_url}/{non_existing_reservation_id}",
                             headers={"Authorization": authorization_token})

    assert (response.status_code == status.HTTP_404_NOT_FOUND
            and response.text == f"Reservation with ID {non_existing_reservation_id} does not exist")


def test_payment_for_trip_reservation_unauthorized(gateway_payments_url):
    response = requests.post(f"{gateway_payments_url}/1234")

    assert (response.status_code == status.HTTP_401_UNAUTHORIZED
            and json.loads(response.content.decode("utf-8"))["detail"] == "Not authenticated")


def test_payment_for_trip_reservation_permission_denied(gateway_payments_url):
    authorization_token = "Bearer IAMBADTOKEN"
    response = requests.post(f"{gateway_payments_url}/1234", headers={"Authorization": authorization_token})

    assert (response.status_code == status.HTTP_403_FORBIDDEN
            and response.text == "User does not have permission to use this service")


def test_payment_for_trip_reservation_success_or_fail(gateway_payments_url, purchase_id, authorization_token):
    sleep(0.1)  # PyTest is faster then RabbitMQ
    response = requests.post(f"{gateway_payments_url}/{purchase_id}",
                             headers={"Authorization": authorization_token})

    if response.status_code == status.HTTP_200_OK:
        response_payload = json.loads(response.content.decode("utf-8"))
        assert (response.status_code == status.HTTP_200_OK
                and response_payload["reservation_id"] == purchase_id
                and response_payload["receipt_id"] == "0987654321")
    else:
        assert (response.status_code == status.HTTP_402_PAYMENT_REQUIRED
                and response.text == f"Payment for reservation with ID {purchase_id} have failed")


def test_payment_for_trip_reservation_expired(gateway_payments_url, purchase_id, authorization_token):
    sleep(60)
    response = requests.post(f"{gateway_payments_url}/{purchase_id}",
                             headers={"Authorization": authorization_token})

    assert (response.status_code == status.HTTP_410_GONE
            and response.text == f"Reservation with ID {purchase_id} has expired")


def test_payment_for_trip_reservation_already_paid_for(gateway_payments_url, purchase_id, authorization_token):
    requests.post(f"{gateway_payments_url}/{purchase_id}",
                  headers={"Authorization": authorization_token})
    response = requests.post(f"{gateway_payments_url}/{purchase_id}",
                             headers={"Authorization": authorization_token})

    assert (response.status_code == status.HTTP_400_BAD_REQUEST
            and response.text == f"Reservation with ID {purchase_id} has already been paid for")
