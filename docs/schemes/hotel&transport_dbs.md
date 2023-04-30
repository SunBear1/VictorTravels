# Schemat baz danych dla serwisów Hotel MS oraz transport MS

**OFERTA TO TURNUS, A WYCIECZKA TO TRIP**

**WYCIECZKA SKŁADA SIĘ Z KILKU TURNUSÓW CZYLI Z OFERT**

**TURNUS TO KONKRETNY WARIANT WYCIECZKI DO HOTELU W OKREŚLONYM PRZEDZIALE CZASOWYM**

# Hotel MS

## Offers

| TripOfferID | TripID | HotelID |
|-------------|--------|---------|
| 1234        | 1      | OSV-XYZ |
| 4212        | 2      | OSV-XYZ |
| 9124        | 3      | BTV-XYZ |
| 1235        | 1      | OSV-TCV |

## RoomsLeft

| ID | HotelID | SmallRoomsLeft | MediumRoomsLeft | LargeRoomsLeft | ApartmentRoomsLeft | StudioRoomsLeft |
|----|---------|----------------|-----------------|----------------|--------------------|-----------------|
| 1  | OSV-XYZ | 2              | 10              | 0              | 15                 | 1               |
| 4  | OSV-TCV | 0              | 2               | 6              | 3                  | 0               |
| 2  | BTV-XYZ | 5              | 1               | 2              | 0                  | 2               |

# Transport MS

## Offers

| TripOfferID | TripID | ConnectionID      | PlacesLeft |
|-------------|--------|-------------------|------------|
| 1234        | 1      | PRS-WAW-TRAIN-XYZ | 28         |
| 1235        | 1      | PRS-WAW-TRAIN-XYZ | 0          |
| 8912        | 5      | ORD-GDN-PLANE-XYZ | 14         |
