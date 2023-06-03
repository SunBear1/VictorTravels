# Test Report

*Report generated on 03-Jun-2023 at 18:09:23 by [pytest-md]* 📝

[pytest-md]: https://github.com/hackebrot/pytest-md

## Summary

36 tests ran in 64.04 seconds ⏱

- 2 failed 😰
- 34 passed 😃

## 2 failed 😰

### tests/api/component/test_trips.py

`test_get_trips_diet_and_arr_region` 0.03s ⏱

```
gateway_trips_url = 'http://localhost:18000/api/v1/trips'

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
    
>       assert (response.status_code == status.HTTP_200_OK
                and response_payload[0]["tripID"] == "5"
                and response_payload[1]["tripID"] == "5")
E       AssertionError: assert (200 == 200 and '1' == '5'
E        +  where 200 = <Response [200]>.status_code
E        +  and   200 = status.HTTP_200_OK
E         - 5
E         + 1)

../tests/api/component/test_trips.py:252: AssertionError
```

`test_get_trips_diet_multiple_diets` 0.05s ⏱

```
gateway_trips_url = 'http://localhost:18000/api/v1/trips'

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
    
>       assert (response.status_code == status.HTTP_200_OK
                and len(response_payload) >= 6)
E       AssertionError: assert (200 == 200 and 4 >= 6)
E        +  where 200 = <Response [200]>.status_code
E        +  and   200 = status.HTTP_200_OK
E        +  and   4 = len([{'bookedUp': False, 'dateFrom': 'Tue Aug 01 00:00:00 GMT 2023', 'dateTo': 'Tue Aug 08 00:00:00 GMT 2023', 'from': {'Gdańsk': {'plane': {'cost': 110, 'id': 'GDN-KNR-PLANE-001', 'seatsLeft': 20, 'transportBookedUp': False}, 'train': None}, 'Kraków': {'plane': {'cost': 105, 'id': 'KRK-KNR-PLANE-001', 'seatsLeft': 20, 'transportBookedUp': False}, 'train': None}, 'Łódź': {'plane': {'cost': 100, 'id': 'LDZ-KNR-PLANE-001', 'seatsLeft': 21, 'transportBookedUp': False}, 'train': None}}, ...}, {'bookedUp': False, 'dateFrom': 'Wed Jul 05 00:00:00 GMT 2023', 'dateTo': 'Sat Jul 15 00:00:00 GMT 2023', 'from': {'Gdańsk': {'plane': {'cost': 78, 'id': 'GDN-GCB-PLANE-001', 'seatsLeft': 1, 'transportBookedUp': False}, 'train': None}, 'Katowice': {'plane': {'cost': 90, 'id': 'KTK-GCB-PLANE-001', 'seatsLeft': 15, 'transportBookedUp': False}, 'train': None}, 'Kraków': {'plane': {'cost': 86, 'id': 'KRK-GCB-PLANE-001', 'seatsLeft': 5, 'transportBookedUp': False}, 'train': None}, 'Warszawa': {'plane': {'cost': 115, 'id': 'WAW-GCB-PLANE-001', 'seatsLeft': 22, 'transportBookedUp': False}, 'train': None}}, ...}, {'bookedUp': False, 'dateFrom': 'Wed Jul 05 00:00:00 GMT 2023', 'dateTo': 'Wed Jul 12 00:00:00 GMT 2023', 'from': {'Gdańsk': {'plane': {'cost': 121, 'id': 'GDN-KGS-PLANE-001', 'seatsLeft': 3, 'transportBookedUp': False}, 'train': None}, 'Katowice': {'plane': {'cost': 105, 'id': 'KTK-KGS-PLANE-001', 'seatsLeft': 10, 'transportBookedUp': False}, 'train': None}, 'Kraków': {'plane': {'cost': 103, 'id': 'KRK-KGS-PLANE-001', 'seatsLeft': 15, 'transportBookedUp': False}, 'train': None}, 'Poznań': {'plane': {'cost': 98, 'id': 'PZN-KGS-PLANE-001', 'seatsLeft': 8, 'transportBookedUp': False}, 'train': None}, ...}, ...}, {'bookedUp': False, 'dateFrom': 'Wed Jul 05 00:00:00 GMT 2023', 'dateTo': 'Sat Jul 15 00:00:00 GMT 2023', 'from': {'Gdańsk': {'plane': {'cost': 121, 'id': 'GDN-KGS-PLANE-001', 'seatsLeft': 3, 'transportBookedUp': False}, 'train': None}, 'Katowice': {'plane': {'cost': 105, 'id': 'KTK-KGS-PLANE-001', 'seatsLeft': 10, 'transportBookedUp': False}, 'train': None}, 'Poznań': {'plane': {'cost': 98, 'id': 'PZN-KGS-PLANE-001', 'seatsLeft': 8, 'transportBookedUp': False}, 'train': None}, 'Warszawa': {'plane': {'cost': 102, 'id': 'WAW-KGS-PLANE-001', 'seatsLeft': 6, 'transportBookedUp': False}, 'train': None}}, ...}])

../tests/api/component/test_trips.py:277: AssertionError
```

## 34 passed 😃

### tests/api/component/test_payments.py

`test_payment_for_trip_reservation_not_found` 0.05s ⏱

`test_payment_for_trip_reservation_unauthorized` 0.01s ⏱

`test_payment_for_trip_reservation_permission_denied` 0.01s ⏱

`test_payment_for_trip_reservation_success_or_fail` 0.17s ⏱

`test_payment_for_trip_reservation_expired` 60.05s ⏱

`test_payment_for_trip_reservation_already_paid_for` 0.05s ⏱

### tests/api/component/test_purchases.py

`test_purchase_trip_reservation_not_found` 0.02s ⏱

`test_purchase_trip_unauthorized` 0.02s ⏱

`test_purchase_trip_permission_denied` 0.01s ⏱

`test_purchase_trip_success` 0.14s ⏱

### tests/api/component/test_reservations.py

`test_make_reservation_success` 0.05s ⏱

`test_make_reservation_insufficient_places` 0.03s ⏱

`test_make_reservation_not_found` 0.02s ⏱

`test_make_reservation_invalid_payload` 0.01s ⏱

`test_make_reservation_unauthorized` 0.01s ⏱

`test_make_reservation_permission_denied` 0.01s ⏱

### tests/api/component/test_trips.py

`test_get_trip` 0.40s ⏱

`test_get_trip_not_exist` 0.03s ⏱

`test_get_trip_price` 0.04s ⏱

`test_get_trip_price_wrong_query` 0.01s ⏱

`test_get_trip_configurations` 0.07s ⏱

`test_get_trips` 0.07s ⏱

`test_get_trips_too_many_guests` 0.03s ⏱

`test_get_trips_not_existing_regions` 0.02s ⏱

`test_get_trips_wrong_dates` 0.04s ⏱

`test_get_trips_no_guests` 0.01s ⏱

`test_get_trips_only_region` 0.03s ⏱

`test_get_trips_only_train_transport` 0.02s ⏱

### tests/api/component/test_users.py

`test_register_user_success` 0.01s ⏱

`test_register_user_already_exists` 0.03s ⏱

`test_register_user_invalid_email` 0.01s ⏱

`test_login_user_success` 0.04s ⏱

`test_login_user_wrong_credentials` 0.03s ⏱

`test_login_user_not_exist` 0.02s ⏱
