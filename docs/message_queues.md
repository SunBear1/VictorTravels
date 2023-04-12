# RabbitMQ messages payload scheme

### Live events

from **Director** to **Gateway**

```json
{
  "bought_trip_id": [
    "trip_12345"
  ],
  "hotel": [
    {
      "hotel_name": "OsovaCourt",
      "hotel_room": "small"
    }
  ],
  "destination": [
    {
      "country": "Toruń",
      "transport_type": "rower"
    }
  ]
}
```

### Trip availability change

from **Director** to **Reservations MS**

operation_type: Add | Delete

```json
{
  "operation_type": "Add",
  "trips_affected": [
    "1234",
    "325325",
    "43534",
    "08453"
  ]
}
```

### Trip reservation request

from **Reservations MS** to **Director**

reserved: true | false

```json
{
  "trip_id": "1234",
  "reserved": true
}
```

### Powiadomienie purchase o rezerwacji

from **Reservations MS** to **Purchase MS**

reserved: true | false

```json
{
  "_id": "example_reservation_id",
  "reserved": true
}
```

### Powiadomienie reservations o wyniku transakcji

from **Purchase MS** to **Reservations MS**

transaction_status: finalized | canceled

```json
{
  "_id": "example_reservation_id",
  "transaction_status": "finalized"
}
```

### Powiadomienie purchase o wyniku płatności

from **Payment MS** to **Purchase MS**

payment: rejected | accepted

```json
{
  "_id": "example_reservation_id",
  "payment": "rejected"
}
```

### Powiadomienie payments o kupnie

from **Purchase MS** to **Payment MS**

purchased: True | False

```json
{
  "_id": "example_reservation_id",
  "purchased": true
}
```

### Powiadomienie payments o czasie rozpoczęcia rezerwacji

from **Purchase MS** to **Payment MS**

purchased: True | False

```json
{
  "_id": "example_reservation_id",
  "reservation_creation_time": "YYYY-MM-DD:HH-MM-SS"
}
```
