# Nazewnictwo baz danych, serwisów oraz ich portów

## Trip Researcher

### Porty

- Wewnątrz klastra - `8000`
- Na zewnątrz klastra - `17999`

### Baza danych

Nazwa: `rsww_17998_trips_db`
Typ: Dokumentowa baza danych MongoDB z jedną kolekcją `trips`

Przykładowy rekord:

```json
{
  "_id": "0001",
  "trip_id": "1",
  "is_booked_up": false,
  "hotel": {
    "hotel_id": "HFP-1",
    "name": "Hotel Fuerteventura Princess",
    "image": "https://i.content4travel.com/cms/img/u/desktop/seres/fueprin_0.jpg?version=1",
    "description": [
      "Zabawa dla całej rodziny",
      "Wyremontowane pokoje i hotelowa infrastruktura",
      "Zadbane baseny z bezpłatnymi leżakami",
      "Strefa wellness tylko dla dorosłych"
    ],
    "diet": {
      "AllInclusive": 900,
      "Breakfast": 200,
      "TwoMeals": 600,
      "None": 0
    },
    "rooms": {
      "small": {
        "cost": 600,
        "available": 20
      },
      "medium": {
        "cost": 200,
        "available": 1
      },
      "large": {
        "cost": 500,
        "available": 3
      },
      "apartment": {
        "cost": 800,
        "available": 0
      },
      "studio": {
        "cost": 1800,
        "available": 1
      }
    }
  },
  "localisation": {
    "country": "Wyspy Kanaryjskie",
    "region": "Fuerteventura"
  },
  "date_from": "01-08-2023",
  "date_to": "08-08-2023",
  "from": {
    "Łódź": {
      "plane": {
        "id": "LDZ-KNR-PLANE-001",
        "cost": 100,
        "seatsLeft": 21,
        "transportBookedUp": false
      }
    },
    "Kraków": {
      "plane": {
        "id": "KRK-KNR-PLANE-001",
        "cost": 105,
        "seatsLeft": 20,
        "transportBookedUp": false
      }
    },
    "Gdańsk": {
      "plane": {
        "id": "GDN-KNR-PLANE-001",
        "cost": 110,
        "seatsLeft": 20,
        "transportBookedUp": false
      }
    }
  },
  "to": {
    "Łódź": {
      "plane": {
        "id": "KNR-LDZ-PLANE-001",
        "cost": 70,
        "seatsLeft": 5,
        "transportBookedUp": false
      }
    },
    "Kraków": {
      "plane": {
        "id": "KNR-KRK-PLANE-001",
        "cost": 90,
        "seatsLeft": 6,
        "transportBookedUp": false
      }
    },
    "Gdańsk": {
      "plane": {
        "id": "KNR-GDN-PLANE-001",
        "cost": 120,
        "seatsLeft": 30,
        "transportBookedUp": false
      }
    }
  }
}
```

## Transport MS

### Baza danych

Nazwa: `rsww_17998_transports`
Typ: Relacyjna baza danych PostgreSQL z dwoma tabelami:

#### Offers

| TripOfferID | TripID | ConnectionID      |
|-------------|--------|-------------------|
| 1234        | 1      | PRS-WAW-TRAIN-XYZ |
| 1235        | 2      | PRS-WAW-TRAIN-XYZ |
| 8912        | 5      | ORD-GDN-PLANE-XYZ |
| 0921        | 3      | WAW-GDN-PLANE-XYZ |

#### SeatsLeft

| ID  | ConnectionID      | SeatsLeft |
|-----|-------------------|-----------|
| 1   | PRS-WAW-TRAIN-XYZ | 2         |
| 3   | ORD-GDN-PLANE-XYZ | 14        |
| 4   | WAW-GDN-PLANE-XYZ | 3         |

## Hotel MS

### Baza danych

Nazwa: `rsww_17998_hotels`
Typ: Relacyjna baza danych PostgreSQL z dwoma tabelami:

#### Offers

| TripOfferID | TripID | HotelID |
|-------------|--------|---------|
| 1234        | 1      | OSV-XYZ |
| 4212        | 2      | OSV-XYZ |
| 9124        | 3      | BTV-XYZ |
| 1235        | 1      | OSV-TCV |

#### RoomsLeft

| ID  | HotelID | SmallRoomsLeft | MediumRoomsLeft | LargeRoomsLeft | ApartmentRoomsLeft | StudioRoomsLeft |
|-----|---------|----------------|-----------------|----------------|--------------------|-----------------|
| 1   | OSV-XYZ | 2              | 10              | 0              | 15                 | 1               |
| 4   | OSV-TCV | 0              | 2               | 6              | 3                  | 0               |
| 2   | BTV-XYZ | 5              | 1               | 2              | 0                  | 2               |

## EventHub MS

### Baza danych

Nazwa: `rsww_17998_events`
Typ: Relacyjna baza danych PostgreSQL z jedną tabelą:

#### EventsLog

| id | type                             | operation | From          | To            | receivedate                | body                                                                                                                                                                                                                                                                                       |
|:---|:---------------------------------|:----------|:--------------|:--------------|:---------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | reservation\_status\_update      | delete    | ReservationMS | EventhubMS    | 2023-05-07 09:25:53.065000 | {"title":"reservation\_status\_update","trip\_offer\_id":"0003","reservation\_id":"64576ea06fdc1980f1be7862","reservation\_status":"created","hotel\_id":"HGR-1","room\_type":"large","connection\_id\_to":"GDN-GCB-PLANE-001","connection\_id\_from":"GCB-GDN-PLANE-001","head\_count":1} |
| 2  | trip\_offer\_hotel\_room\_update | delete    | EventhubMS    | HotelMS       | 2023-05-07 09:25:53.077000 | {"title":"trip\_offer\_hotel\_room\_update","trip\_offer\_id":"0003","operation\_type":"delete","hotel\_id":"HGR-1","room\_type":"large"}                                                                                                                                                  |
| 3  | trip\_offer\_transport\_update   | delete    | EventhubMS    | TransportMS   | 2023-05-07 09:25:53.084000 | {"title":"trip\_offer\_transport\_update","trip\_offer\_id":"0003","operation\_type":"delete","connection\_id\_to":"GDN-GCB-PLANE-001","connection\_id\_from":"GCB-GDN-PLANE-001","head\_count":1}                                                                                         |
| 4  | transport\_booking\_status       | delete    | TransportMS   | EventhubMS    | 2023-05-07 09:25:53.140000 | {"title":"transport\_booking\_status","trip\_offers\_id":\[\],"connection\_id":"GDN-GCB-PLANE-001","is\_transport\_booked\_up":true}                                                                                                                                                       |
| 5  | transport\_booking\_status       | delete    | EventhubMS    | ReservationMS | 2023-05-07 09:25:53.143000 | {"title":"transport\_booking\_status","operation\_type":"delete","trip\_offers\_affected":\[\],"connection\_id":"GDN-GCB-PLANE-001"}                                                                                                                                                       |
| 6  | reservation\_status\_update      | add       | ReservationMS | EventhubMS    | 2023-05-07 09:26:52.932000 | {"title":"reservation\_status\_update","trip\_offer\_id":"0003","reservation\_id":"64576ea06fdc1980f1be7862","reservation\_status":"expired","head\_count":0}                                                                                                                              |
| 7  | trip\_offer\_hotel\_room\_update | add       | EventhubMS    | HotelMS       | 2023-05-07 09:26:52.949000 | {"title":"trip\_offer\_hotel\_room\_update","trip\_offer\_id":"0003","operation\_type":"add","hotel\_id":"HGR-1","room\_type":"large"}                                                                                                                                                     |
| 8  | trip\_offer\_transport\_update   | add       | EventhubMS    | TransportMS   | 2023-05-07 09:26:52.952000 | {"title":"trip\_offer\_transport\_update","trip\_offer\_id":"0003","operation\_type":"add","connection\_id\_to":"GDN-GCB-PLANE-001","connection\_id\_from":"GCB-GDN-PLANE-001","head\_count":1}                                                                                            |
| 9  | transport\_booking\_status       | add       | TransportMS   | EventhubMS    | 2023-05-07 09:26:52.998000 | {"title":"transport\_booking\_status","trip\_offers\_id":\[\],"connection\_id":"GDN-GCB-PLANE-001","is\_transport\_booked\_up":false}                                                                                                                                                      |
| 10 | transport\_booking\_status       | add       | EventhubMS    | ReservationMS | 2023-05-07 09:26:53.000000 | {"title":"transport\_booking\_status","operation\_type":"add","trip\_offers\_affected":\[\],"connection\_id":"GDN-GCB-PLANE-001"}                                                                                                                                                          |

#### TripsForLiveEvents

| OfferID | TripID | HotelID  | HotelName                                 | Country           | Region        |
|---------|:-------|:---------|:------------------------------------------|:------------------|---------------|
| 1       | 1      | HFP-1    | Hotel Fuerteventura Princess              | Wyspy Kanaryjskie | Fuerteventura |
| 2       | 2      | HAB-1    | Hotel Alhambra                            | Hiszpania         | Costa Brava   |
| 3       | 3      | HGR-1    | Hotel Gaia Royal                          | Grecja            | Kos           |
| 4       | 4      | HSMKB-1  | Hotel Smy Kos Beach & Splash              | Grecja            | Kos           |
| 5       | 5      | HHINER-1 | Hotel Holiday Inn Express Rzeszów Airport | Polska            | Rzeszów       |
| 6       | 5      | HHINER-2 | Hotel Holiday Inn Express Rzeszów Airport | Polska            | Rzeszów       |

### Reservations MS

### Porty

- Wewnątrz klastra - `8001`
- Na zewnątrz klastra - `18001`

### Baza danych

Nazwa: `rsww_17998_reservations_db`
Typ: Dokumentowa baza danych MongoDB z dwoma kolekcjami:

#### Reservations

Przykładowy rekord:

```json
{
  "_id": {
    "$oid": "6457710e2b8e43d24be92b34"
  },
  "head_count": 1,
  "reservation_creation_time": "2023-05-07T09:36:14.993297",
  "reservation_status": "temporary",
  "trip_offer_id": "0003",
  "uid": "example_uid"
}
```

#### TripOffers

Rekord dla dostępnych hoteli:

```json
{
  "_id": "available_connections",
  "GCB-GDN-PLANE-001": 32,
  "GCB-KRK-PLANE-001": 8,
  "GCB-KTK-PLANE-001": 4,
  "GCB-WAW-PLANE-001": 15,
  "GDN-GCB-PLANE-001": 1,
  "GDN-KGS-PLANE-001": 3
}
```

Rekord dla dostępnych połączeń:

```json
  {
  "_id": "available_hotels",
  "HAB-1": {
    "smallroomsleft": 3,
    "mediumroomsleft": 9,
    "largeroomsleft": 20,
    "apartmentroomsleft": 5,
    "studioroomsleft": 15
  },
  "HFP-1": {
    "smallroomsleft": 20,
    "mediumroomsleft": 1,
    "largeroomsleft": 3,
    "apartmentroomsleft": 0,
    "studioroomsleft": 1
  }
}
```

### Purchase MS

### Baza danych

Nazwa: `rsww_17998_purchases_db`
Typ: Dokumentowa baza danych MongoDB z dwoma kolekcjami:

#### Purchases

Przykładowy rekord:

```json
{
  "_id": {
    "$oid": "6457710e2b8e43d24be92b34"
  },
  "payment_status": "pending",
  "price": 2137.69,
  "purchase_status": "pending",
  "trip_offer_id": "0003",
  "uid": "example_uid"
}
```

### Porty

- Wewnątrz klastra - `8002`
- Na zewnątrz klastra - `18002`

### Payment MS

### Baza danych

Nazwa: `rsww_17998_payments_db`
Typ: Dokumentowa baza danych MongoDB z dwoma kolekcjami:

#### Payments

Przykładowy rekord:

```json
{
  "_id": {
    "$oid": "6457729a2b8e43d24be92b37"
  },
  "payment_status": "accepted",
  "price": 2137.69,
  "purchase_status": "confirmed",
  "reservation_creation_time": "2023-05-07T09:42:50.471977",
  "uid": "example_uid",
  "trip_offer_id": "0003"
}
```

### Porty

- Wewnątrz klastra - `8003`
- Na zewnątrz klastra - `18003`

### Gateway

### Baza danych

Nazwa: `rsww_17998_users`
Typ: Relacyjna baza danych PostgreSQL z jedną tabelą:

#### Users

| id  | login                     | password                                                         |
|:----|:--------------------------|:-----------------------------------------------------------------|
| 1   | example\_user@example.com | 94518f7a6830ddcd21a7fsa821f9dbfa3bb50a69663146a554df9cdd182bcb51 |
| 2   | wiktor@interia.pl         | 94518f7a68fadsdcd21a76fd821f9dbfa3bb50a69663146a55gdsfd4d182bcb3 |
| 3   | admin@wp.pl               | 94518f7a6830ddcd21a76ad821f2dbfa3bb50a69663146a551df9cdd182bcb53 |
| 4   | ryan.gosling@luxury.com   | 94518f7a6830ddcd21a76fd821f9dbfa3bb50a69663146a554df9cdd182bcb54 |

### Porty

- Wewnątrz klastra - `8080`
- Na zewnątrz klastra - `18000`

### Message Broker

### Porty

#### AMQP

- Wewnątrz klastra - `5672`
- Na zewnątrz klastra - `17998`

#### UI

- Wewnątrz klastra - `15672`
- Na zewnątrz klastra - `18004`

### GUI

### Porty

- Wewnątrz klastra - `80`
- Na zewnątrz klastra - `18005`
