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
