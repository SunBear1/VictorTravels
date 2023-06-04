# Test Report

*Report generated on 04-Jun-2023 at 02:23:01 by [pytest-md]* 📝

[pytest-md]: https://github.com/hackebrot/pytest-md

## Summary

36 tests ran in 63.51 seconds ⏱

- 36 passed 😃

## 36 passed 😃

### tests/api/component/test_payments.py

`test_payment_for_trip_reservation_not_found` 0.03s ⏱

`test_payment_for_trip_reservation_unauthorized` 0.01s ⏱

`test_payment_for_trip_reservation_permission_denied` 0.01s ⏱

`test_payment_for_trip_reservation_success_or_fail` 0.16s ⏱

`test_payment_for_trip_reservation_expired` 60.07s ⏱

`test_payment_for_trip_reservation_already_paid_for` 0.10s ⏱

### tests/api/component/test_purchases.py

`test_purchase_trip_reservation_not_found` 0.03s ⏱

`test_purchase_trip_unauthorized` 0.01s ⏱

`test_purchase_trip_permission_denied` 0.01s ⏱

`test_purchase_trip_success` 0.16s ⏱

### tests/api/component/test_reservations.py

`test_make_reservation_success` 0.05s ⏱

`test_make_reservation_insufficient_places` 0.03s ⏱

`test_make_reservation_not_found` 0.05s ⏱

`test_make_reservation_invalid_payload` 0.01s ⏱

`test_make_reservation_unauthorized` 0.01s ⏱

`test_make_reservation_permission_denied` 0.01s ⏱

### tests/api/component/test_trips.py

`test_get_trip` 0.04s ⏱

`test_get_trip_not_exist` 0.03s ⏱

`test_get_trip_price` 0.04s ⏱

`test_get_trip_price_wrong_query` 0.01s ⏱

`test_get_trip_configurations` 0.06s ⏱

`test_get_trips` 0.06s ⏱

`test_get_trips_too_many_guests` 0.02s ⏱

`test_get_trips_not_existing_regions` 0.03s ⏱

`test_get_trips_wrong_dates` 0.07s ⏱

`test_get_trips_no_guests` 0.01s ⏱

`test_get_trips_only_region` 0.04s ⏱

`test_get_trips_only_train_transport` 0.05s ⏱

`test_get_trips_diet_and_arr_region` 0.05s ⏱

`test_get_trips_diet_multiple_diets` 0.06s ⏱

### tests/api/component/test_users.py

`test_register_user_success` 0.03s ⏱

`test_register_user_already_exists` 0.05s ⏱

`test_register_user_invalid_email` 0.01s ⏱

`test_login_user_success` 0.04s ⏱

`test_login_user_wrong_credentials` 0.04s ⏱

`test_login_user_not_exist` 0.02s ⏱
