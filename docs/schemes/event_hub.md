# Schemat baz danych dla Event HUB'a

| ID | Title                   | Operation | From          | ReceiveDate         | Body                                                      |
|----|-------------------------|-----------|---------------|---------------------|-----------------------------------------------------------|
| 1  | ReservationStatusUpdate | created   | ReservationMS | 2023-04-27T17:22:10 | {"trip_offer_id": "1234","reservation_status": "created"} |
| 2  | AvailableOffersUpdate   | add       | HotelMS       | 2023-04-27T17:21:10 | {"operation": "add","trip_offers_id": ["1234","4312"]}    |
| 3  | AvailableOffersUpdate   | delete    | TransportMS   | 2023-04-27T17:21:10 | {"operation": "delete","trip_offers_id": ["2311","2137"]} |



