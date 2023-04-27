# Schemat payloadów wiadomości

## Messages from **Event HUB**

### Zmiana dostępnych wycieczek do kupienia/rezerwacji

operation_type: Add | Delete
trips_affected: ID konkretnej wycieczki, czyli turnusu
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

### Kupno/rezerwacja hotelu

```json
{
  "trip_id": "1234"
}
```

### Kupno/rezerwacja transportu

```json
{
  "trip_id": "1234"
}
```

## Messages from **Reservations MS**

### Informacje o statusie rezerwacji

```json
{
  "trip_id": "1234",
  "reservation_status": "created"
  |
  "canceled"
  |
  "expired"
  |
  "bought"
}
```

### Powiadomienie o stworzonej rezerwacji

```json
{
  "_id": "example_reservation_id",
  "trip_id": "1234"
}
```

### Powiadomienie o czasie stworzenie rezerwacji

```json
{
  "_id": "example_reservation_id",
  "reservation_creation_time": "2023-04-27T17:22:10.936561"
}
```

## Messages from **Purchase MS**

transaction_status: finalized | canceled

```json
{
  "_id": "example_reservation_id",
  "transaction_status": "finalized"
}
```

### Powiadomienie o kupnie wycieczki

```json
{
  "_id": "example_reservation_id",
  "trip_id": "1234",
  "purchase_status": "confirmed"
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

### Powiadomienie payments o czasie rozpoczęcia rezerwacji

from **Purchase MS** to **Payment MS**

purchased: True | False

```json
{
  "_id": "example_reservation_id",
  "reservation_creation_time": "YYYY-MM-DD:HH-MM-SS"
}
```
