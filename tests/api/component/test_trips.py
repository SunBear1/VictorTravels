import json

import requests
from starlette import status


def test_get_trip(gateway_trips_url):
    trip_offer_id = "0001"
    response = requests.get(f"{gateway_trips_url}/trip/{trip_offer_id}")

    response_payload = json.loads(response.content.decode("utf-8"))
    assert (response.status_code == status.HTTP_200_OK
            and response_payload["id"] == trip_offer_id
            and response_payload["tripID"] == "1")


def test_get_trip_not_exist(gateway_trips_url):
    trip_offer_id = "0000"
    response = requests.get(f"{gateway_trips_url}/trip/{trip_offer_id}")

    assert (response.status_code == status.HTTP_404_NOT_FOUND
            and response.text == f"Trip with ID {trip_offer_id} does not exist")


def test_get_trip_price(gateway_trips_url):
    expected_price: float = 18975.0
    query_params = {
        "adults": 2,
        "kids_to_3yo": 0,
        "kids_to_10yo": 0,
        "kids_to_18yo": 0,
        "number_of_days": 7,
        "room_cost": 600,
        "diet_cost": 600,
        "transport_to_cost": 120,
        "transport_from_cost": 105
    }
    response = requests.get(f"{gateway_trips_url}/price", params=query_params,
                            timeout=3.00,
                            verify=False)

    assert (response.status_code == status.HTTP_200_OK
            and float(response.text) == expected_price)


def test_get_trip_price_wrong_query(gateway_trips_url):
    query_params = {
        "adults": -5,
    }
    response = requests.get(f"{gateway_trips_url}/price", params=query_params,
                            timeout=3.00,
                            verify=False)

    assert (response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY)


def test_get_trip_configurations(gateway_trips_url):
    response = requests.get(f"{gateway_trips_url}/configurations",
                            timeout=3.00,
                            verify=False)
    response_payload = json.loads(response.content.decode("utf-8"))

    assert (response.status_code == status.HTTP_200_OK
            and len(response_payload["departureLocations"]) > 1
            and len(response_payload["arrivalLocations"]) > 1
            and len(response_payload["transportTypes"]) > 1
            )


def test_get_trips(gateway_trips_url):
    query_params = {
        "adults": 1,
        "kids_ro_3yo": 0,
        "kids_to_10yo": 0,
        "kids_to_18yo": 0,
        "date_from": None,
        "date_to": None,
        "departure_region": None,
        "arrival_region": None,
        "transport": None,
        "diet": None,
        "max_price": None
    }
    response = requests.get(f"{gateway_trips_url}", params=query_params,
                            timeout=3.00,
                            verify=False)

    assert response.status_code == status.HTTP_200_OK


def test_get_trips_too_many_guests(gateway_trips_url):
    query_params = {
        "adults": 100,
        "kids_ro_3yo": 100,
        "kids_to_10yo": 100,
        "kids_to_18yo": 100,
        "date_from": None,
        "date_to": None,
        "departure_region": None,
        "arrival_region": None,
        "transport": None,
        "diet": None,
        "max_price": None
    }
    response = requests.get(f"{gateway_trips_url}", params=query_params,
                            timeout=3.00,
                            verify=False)
    response_payload = json.loads(response.content.decode("utf-8"))

    assert (response.status_code == status.HTTP_200_OK
            and not response_payload)


def test_get_trips_not_existing_regions(gateway_trips_url):
    query_params = {
        "adults": 1,
        "kids_ro_3yo": 0,
        "kids_to_10yo": 0,
        "kids_to_18yo": 0,
        "date_from": None,
        "date_to": None,
        "departure_region": None,
        "arrival_region": "Not existing place",
        "transport": None,
        "diet": None,
        "max_price": None
    }
    response = requests.get(f"{gateway_trips_url}", params=query_params,
                            timeout=3.00,
                            verify=False)

    response_payload = json.loads(response.content.decode("utf-8"))

    assert (response.status_code == status.HTTP_200_OK
            and not response_payload)


def test_get_trips_wrong_dates(gateway_trips_url):
    query_params = {
        "adults": 1,
        "kids_ro_3yo": 0,
        "kids_to_10yo": 0,
        "kids_to_18yo": 0,
        "date_from": "2025-06-30",
        "date_to": "2025-06-30",
        "departure_region": None,
        "arrival_region": None,
        "transport": None,
        "diet": None,
        "max_price": None
    }
    response = requests.get(f"{gateway_trips_url}", params=query_params,
                            timeout=3.00,
                            verify=False)

    response_payload = json.loads(response.content.decode("utf-8"))

    assert (response.status_code == status.HTTP_200_OK
            and not response_payload)


def test_get_trips_no_guests(gateway_trips_url):
    query_params = {
        "adults": 0,
        "kids_ro_3yo": 0,
        "kids_to_10yo": 0,
        "kids_to_18yo": 0,
        "date_from": None,
        "date_to": None,
        "departure_region": None,
        "arrival_region": None,
        "transport": None,
        "diet": None,
        "max_price": None
    }
    response = requests.get(f"{gateway_trips_url}", params=query_params,
                            timeout=3.00,
                            verify=False)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_trips_only_region(gateway_trips_url):
    query_params = {
        "adults": 1,
        "kids_ro_3yo": 0,
        "kids_to_10yo": 0,
        "kids_to_18yo": 0,
        "date_from": None,
        "date_to": None,
        "departure_region": None,
        "arrival_region": "Wyspy Kanaryjskie",
        "transport": None,
        "diet": None,
        "max_price": None
    }
    response = requests.get(f"{gateway_trips_url}", params=query_params,
                            timeout=3.00,
                            verify=False)

    response_payload = json.loads(response.content.decode("utf-8"))

    assert (response.status_code == status.HTTP_200_OK
            and response_payload[0]["tripID"] == "1")


def test_get_trips_only_train_transport(gateway_trips_url):
    query_params = {
        "adults": 1,
        "kids_ro_3yo": 0,
        "kids_to_10yo": 0,
        "kids_to_18yo": 0,
        "date_from": None,
        "date_to": None,
        "departure_region": None,
        "arrival_region": None,
        "transport": "train",
        "diet": None,
        "max_price": None
    }
    response = requests.get(f"{gateway_trips_url}", params=query_params,
                            timeout=3.00,
                            verify=False)

    response_payload = json.loads(response.content.decode("utf-8"))

    assert (response.status_code == status.HTTP_200_OK
            and response_payload[0]["tripID"] == "5"
            and response_payload[1]["tripID"] == "5")


def test_get_trips_diet_and_arr_region(gateway_trips_url):
    query_params = {
        "adults": 1,
        "kids_ro_3yo": 0,
        "kids_to_10yo": 0,
        "kids_to_18yo": 0,
        "date_from": None,
        "date_to": None,
        "departure_region": None,
        "arrival_region": "Polska",
        "transport": None,
        "diet": "Breakfast",
        "max_price": None
    }
    response = requests.get(f"{gateway_trips_url}", params=query_params,
                            timeout=3.00,
                            verify=False)

    response_payload = json.loads(response.content.decode("utf-8"))

    assert (response.status_code == status.HTTP_200_OK
            and response_payload[0]["tripID"] == "5"
            and response_payload[1]["tripID"] == "5")


def test_get_trips_diet_multiple_diets(gateway_trips_url):
    query_params = {
        "adults": 2,
        "kids_ro_3yo": 0,
        "kids_to_10yo": 0,
        "kids_to_18yo": 0,
        "date_from": None,
        "date_to": None,
        "departure_region": None,
        "arrival_region": None,
        "transport": None,
        "diet": ["Breakfast", "AllInclusive"],
        "max_price": None
    }
    response = requests.get(f"{gateway_trips_url}", params=query_params,
                            timeout=3.00,
                            verify=False)

    response_payload = json.loads(response.content.decode("utf-8"))

    assert (response.status_code == status.HTTP_200_OK
            and len(response_payload) >= 6)
