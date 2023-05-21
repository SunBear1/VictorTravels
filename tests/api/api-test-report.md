# Test Report

*Report generated on 21-May-2023 at 11:30:43 by [pytest-md]* 📝

[pytest-md]: https://github.com/hackebrot/pytest-md

## Summary

24 tests ran in 61.75 seconds ⏱

- 24 passed 😃

## 24 passed 😃

### tests/api/component/test_payments.py

`test_payment_for_trip_reservation_not_found` 0.01s ⏱

`test_payment_for_trip_reservation_unauthorized` 0.00s ⏱

`test_payment_for_trip_reservation_permission_denied` 0.00s ⏱

`test_payment_for_trip_reservation_success_or_fail` 0.12s ⏱

`test_payment_for_trip_reservation_expired` 60.07s ⏱

`test_payment_for_trip_reservation_already_paid_for` 0.02s ⏱

### tests/api/component/test_purchases.py

`test_purchase_trip_reservation_not_found` 0.01s ⏱

`test_purchase_trip_unauthorized` 0.01s ⏱

`test_purchase_trip_permission_denied` 0.00s ⏱

`test_purchase_trip_success` 0.12s ⏱

### tests/api/component/test_reservations.py

`test_make_reservation_success` 0.02s ⏱

`test_make_reservation_insufficient_places` 0.01s ⏱

`test_make_reservation_not_found` 0.01s ⏱

`test_make_reservation_invalid_payload` 0.00s ⏱

`test_make_reservation_unauthorized` 0.00s ⏱

`test_make_reservation_permission_denied` 0.00s ⏱

### tests/api/component/test_trips.py

`test_get_trip` 0.01s ⏱

`test_get_trip_not_exist` 0.01s ⏱

### tests/api/component/test_users.py

`test_register_user_success` 0.01s ⏱

`test_register_user_already_exists` 0.01s ⏱

`test_register_user_invalid_email` 0.00s ⏱

`test_login_user_success` 0.01s ⏱

`test_login_user_wrong_credentials` 0.01s ⏱

`test_login_user_not_exist` 0.01s ⏱
