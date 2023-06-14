# Test Report

*Report generated on 14-Jun-2023 at 19:09:06 by [pytest-md]* 📝

[pytest-md]: https://github.com/hackebrot/pytest-md

## Summary

37 tests ran in 62.27 seconds ⏱

- 1 failed 😰
- 36 passed 😃

## 1 failed 😰

### tests/api/component/test_trips.py

`test_get_trips_max_price_bigger_than_price` 0.01s ⏱

```
gateway_trips_url = 'http://localhost:18000/api/v1/trips'

    def test_get_trips_max_price_bigger_than_price(gateway_trips_url):
        query_params = {
            "adults": 1,
            "kids_to_3yo": 0,
            "kids_to_10yo": 0,
            "kids_to_18yo": 0,
            "date_from": None,
            "date_to": None,
            "departure_region": None,
            "arrival_region": None,
            "transport": None,
            "diet": None,
            "max_price": 1100
        }
        response = requests.get(f"{gateway_trips_url}", params=query_params,
                                timeout=3.00,
                                verify=False)
    
        response_payload = json.loads(response.content.decode("utf-8"))
    
>       assert (response.status_code == status.HTTP_200_OK
                and response_payload[3]["price"] == 1089)
E       assert (200 == 200 and None == 1089)
E        +  where 200 = <Response [200]>.status_code
E        +  and   200 = status.HTTP_200_OK

../tests/api/component/test_trips.py:301: AssertionError
```

## 36 passed 😃

### tests/api/component/test_payments.py

`test_payment_for_trip_reservation_not_found` 0.01s ⏱

`test_payment_for_trip_reservation_unauthorized` 0.00s ⏱

`test_payment_for_trip_reservation_permission_denied` 0.00s ⏱

`test_payment_for_trip_reservation_success_or_fail` 0.12s ⏱

`test_payment_for_trip_reservation_expired` 60.04s ⏱

`test_payment_for_trip_reservation_already_paid_for` 0.02s ⏱

### tests/api/component/test_purchases.py

`test_purchase_trip_reservation_not_found` 0.01s ⏱

`test_purchase_trip_unauthorized` 0.00s ⏱

`test_purchase_trip_permission_denied` 0.00s ⏱

`test_purchase_trip_success` 0.12s ⏱

### tests/api/component/test_reservations.py

`test_make_reservation_success` 0.02s ⏱

`test_make_reservation_insufficient_places` 0.02s ⏱

`test_make_reservation_not_found` 0.01s ⏱

`test_make_reservation_invalid_payload` 0.00s ⏱

`test_make_reservation_unauthorized` 0.00s ⏱

`test_make_reservation_permission_denied` 0.00s ⏱

### tests/api/component/test_trips.py

`test_get_trip` 0.19s ⏱

`test_get_trip_not_exist` 0.01s ⏱

`test_get_trip_price` 0.01s ⏱

`test_get_trip_price_wrong_query` 0.00s ⏱

`test_get_trip_configurations` 0.02s ⏱

`test_get_trips` 0.03s ⏱

`test_get_trips_too_many_guests` 0.01s ⏱

`test_get_trips_not_existing_regions` 0.01s ⏱

`test_get_trips_wrong_dates` 0.01s ⏱

`test_get_trips_no_guests` 0.00s ⏱

`test_get_trips_only_region` 0.01s ⏱

`test_get_trips_only_train_transport` 0.02s ⏱

`test_get_trips_diet_and_arr_region` 0.01s ⏱

`test_get_trips_diet_multiple_diets` 0.02s ⏱

### tests/api/component/test_users.py

`test_register_user_success` 0.01s ⏱

`test_register_user_already_exists` 0.01s ⏱

`test_register_user_invalid_email` 0.00s ⏱

`test_login_user_success` 0.01s ⏱

`test_login_user_wrong_credentials` 0.01s ⏱

`test_login_user_not_exist` 0.01s ⏱
