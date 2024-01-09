# Test Report

*Report generated on 09-Jan-2024 at 12:35:16 by [pytest-md]* 📝

[pytest-md]: https://github.com/hackebrot/pytest-md

## Summary

37 tests ran in 65.00 seconds ⏱

- 37 passed 😃

## 37 passed 😃

### tests/api/component/test_payments.py

`test_payment_for_trip_reservation_not_found` 0.03s ⏱

`test_payment_for_trip_reservation_unauthorized` 0.01s ⏱

`test_payment_for_trip_reservation_permission_denied` 0.01s ⏱

`test_payment_for_trip_reservation_success_or_fail` 0.15s ⏱

`test_payment_for_trip_reservation_expired` 60.04s ⏱

`test_payment_for_trip_reservation_already_paid_for` 0.07s ⏱

### tests/api/component/test_purchases.py

`test_purchase_trip_reservation_not_found` 0.02s ⏱

`test_purchase_trip_unauthorized` 0.02s ⏱

`test_purchase_trip_permission_denied` 0.01s ⏱

`test_purchase_trip_success` 0.15s ⏱

### tests/api/component/test_reservations.py

`test_make_reservation_success` 0.08s ⏱

`test_make_reservation_insufficient_places` 0.03s ⏱

`test_make_reservation_not_found` 0.04s ⏱

`test_make_reservation_invalid_payload` 0.01s ⏱

`test_make_reservation_unauthorized` 0.01s ⏱

`test_make_reservation_permission_denied` 0.01s ⏱

### tests/api/component/test_trips.py

`test_get_trip` 1.13s ⏱

`test_get_trip_not_exist` 0.03s ⏱

`test_get_trip_price` 0.07s ⏱

`test_get_trip_price_wrong_query` 0.01s ⏱

`test_get_trip_configurations` 0.06s ⏱

`test_get_trips` 0.08s ⏱

`test_get_trips_too_many_guests` 0.02s ⏱

`test_get_trips_not_existing_regions` 0.04s ⏱

`test_get_trips_wrong_dates` 0.05s ⏱

`test_get_trips_no_guests` 0.01s ⏱

`test_get_trips_only_region` 0.05s ⏱

`test_get_trips_only_train_transport` 0.04s ⏱

`test_get_trips_diet_and_arr_region` 0.07s ⏱

`test_get_trips_diet_multiple_diets` 0.09s ⏱

`test_get_trips_max_price_bigger_than_price` 0.07s ⏱

### tests/api/component/test_users.py

`test_register_user_success` 0.05s ⏱

`test_register_user_already_exists` 0.08s ⏱

`test_register_user_invalid_email` 0.02s ⏱

`test_login_user_success` 0.07s ⏱

`test_login_user_wrong_credentials` 0.09s ⏱

`test_login_user_not_exist` 0.07s ⏱
