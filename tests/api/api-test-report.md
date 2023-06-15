# Test Report

*Report generated on 15-Jun-2023 at 19:14:04 by [pytest-md]* 📝

[pytest-md]: https://github.com/hackebrot/pytest-md

## Summary

37 tests ran in 62.05 seconds ⏱

- 37 passed 😃

## 37 passed 😃

### tests/api/component/test_payments.py

`test_payment_for_trip_reservation_not_found` 0.03s ⏱

`test_payment_for_trip_reservation_unauthorized` 0.01s ⏱

`test_payment_for_trip_reservation_permission_denied` 0.01s ⏱

`test_payment_for_trip_reservation_success_or_fail` 0.14s ⏱

`test_payment_for_trip_reservation_expired` 60.04s ⏱

`test_payment_for_trip_reservation_already_paid_for` 0.04s ⏱

### tests/api/component/test_purchases.py

`test_purchase_trip_reservation_not_found` 0.02s ⏱

`test_purchase_trip_unauthorized` 0.01s ⏱

`test_purchase_trip_permission_denied` 0.01s ⏱

`test_purchase_trip_success` 0.13s ⏱

### tests/api/component/test_reservations.py

`test_make_reservation_success` 0.03s ⏱

`test_make_reservation_insufficient_places` 0.02s ⏱

`test_make_reservation_not_found` 0.02s ⏱

`test_make_reservation_invalid_payload` 0.01s ⏱

`test_make_reservation_unauthorized` 0.00s ⏱

`test_make_reservation_permission_denied` 0.01s ⏱

### tests/api/component/test_trips.py

`test_get_trip` 0.01s ⏱

`test_get_trip_not_exist` 0.01s ⏱

`test_get_trip_price` 0.02s ⏱

`test_get_trip_price_wrong_query` 0.01s ⏱

`test_get_trip_configurations` 0.02s ⏱

`test_get_trips` 0.02s ⏱

`test_get_trips_too_many_guests` 0.01s ⏱

`test_get_trips_not_existing_regions` 0.01s ⏱

`test_get_trips_wrong_dates` 0.02s ⏱

`test_get_trips_no_guests` 0.01s ⏱

`test_get_trips_only_region` 0.01s ⏱

`test_get_trips_only_train_transport` 0.02s ⏱

`test_get_trips_diet_and_arr_region` 0.02s ⏱

`test_get_trips_diet_multiple_diets` 0.02s ⏱

`test_get_trips_max_price_bigger_than_price` 0.02s ⏱

### tests/api/component/test_users.py

`test_register_user_success` 0.01s ⏱

`test_register_user_already_exists` 0.02s ⏱

`test_register_user_invalid_email` 0.01s ⏱

`test_login_user_success` 0.02s ⏱

`test_login_user_wrong_credentials` 0.02s ⏱

`test_login_user_not_exist` 0.01s ⏱
