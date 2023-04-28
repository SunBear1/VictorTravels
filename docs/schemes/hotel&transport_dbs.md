# Schemat baz danych dla serwisów Hotel MS oraz transport MS

**OFERTA TO TURNUS, A WYCIECZKA TO TRIP**

**WYCIECZKA SKŁADA SIĘ Z KILKU TURNUSÓW CZYLI Z OFERT**

**TURNUS TO KONKRETNY WARIANT WYCIECZKI DO HOTELU W OKREŚLONYM PRZEDZIALE CZASOWYM**

# Hotel MS

## Offers

| ID | TripID | HotelID | SmallRoomsLeft | MediumRoomsLeft | LargeRoomsLeft | ApartmentRoomsLeft | StudioRoomsLeft |
|----|--------|---------|----------------|-----------------|----------------|--------------------|-----------------|
| 1  | 1234   | OSV     | 2              | 10              | 0              | 15                 | 1               |
| 4  | 1234   | OSV     | 0              | 2               | 6              | 3                  | 0               |
| 2  | 7632   | BTV     | 5              | 1               | 2              | 0                  | 2               |

# Transport MS

## Offers

| ID | TripID | ConnectionID      | PlacesLeft |
|----|--------|-------------------|------------|
| 1  | 1234   | PRS-WAW-TRAIN-XYZ | 28         |
| 3  | 1234   | PRS-WAW-TRAIN-XYZ | 0          |
| 5  | 8912   | ORD-GDN-PLANE-XYZ | 14         |
