# Schemat payloadów wiadomości

## Messages from **Event HUB**

### Zmiana dostępnych wycieczek do kupienia/rezerwacji

trips_affected: ID konkretnej wycieczki, czyli turnusu

```json
{
  "operation_type": "add|delete",
  "trip_offers_affected": [
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
  "trip_offer_id": "1234",
  "operation_type": "add|delete",
  "room_type": "small|medium|large|apartment|studio"
}
```

### Kupno/rezerwacja transportu

```json
{
  "trip_offer_id": "1234",
  "connection_id": "PRS-WAW-TRAIN-XYZ"
}
```

## Messages from **Reservations MS**

### Informacje o statusie rezerwacji

```json
{
  "trip_offer_id": "1234",
  "reservation_status": "created|canceled|expired|finalized"
}
```

### Powiadomienie o stworzonej rezerwacji

```json
{
  "_id": "example_reservation_id",
  "trip_offer_id": "1234"
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

```json
{
  "_id": "example_reservation_id",
  "transaction_status": "finalized|canceled|expired"
}
```

### Powiadomienie o kupnie wycieczki

```json
{
  "_id": "example_reservation_id",
  "offers_id": "1234",
  "purchase_status": "confirmed"
}
```

## Messages from **Payment MS**

### Powiadomienie o wyniku płatności

```json
{
  "_id": "example_reservation_id",
  "payment": "rejected|accepted|expired"
}
```

## Messages from **Hotel MS**

### Wiadomość o aktualizacji miejsc w wycieczkach TRIPS DB

Ta wiadomość jest wysyłana za każdym razem jak miejsce w wycieczce ulegną zmianie

```json
{
  "operation_type": "add|delete",
  "trip_offers_id": [
    "1234",
    "4312"
  ]
}
```

### Wiadomość o aktualizacji dostępnych wycieczek

Ta wiadomość jest wysyłana kiedy miejsca w jakiejś wycieczce są równe zero, lub właśnie zmieniły się z 0 na więcej

```json
{
  "operation_type": "add|delete",
  "trip_offers_id": [
    "1234",
    "4312"
  ]
}
```

## Messages from **Transport MS**

### Wiadomość o aktualizacji miejsc w wycieczkach TRIPS DB

Ta wiadomość jest wysyłana za każdym razem jak miejsce w wycieczce ulegną zmianie

```json
{
  "operation_type": "add|delete",
  "trip_offers_id": [
    "1234",
    "4312"
  ]
}
```

### Wiadomość o aktualizacji dostępnych wycieczek

Ta wiadomość jest wysyłana kiedy miejsca w jakiejś wycieczce są równe zero, lub właśnie zmieniły się z 0 na więcej

```json
{
  "operation_type": "add|delete",
  "trip_offers_id": [
    "1234",
    "4312"
  ]
}
```
