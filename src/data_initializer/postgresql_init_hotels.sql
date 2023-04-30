CREATE TABLE Offers
(
    TripOfferID        varchar(50) PRIMARY KEY,
    TripID             varchar(50),
    HotelID            varchar(50),
    SmallRoomsLeft     integer,
    MediumRoomsLeft    integer,
    LargeRoomsLeft     integer,
    ApartmentRoomsLeft integer,
    StudioRoomsLeft    integer
);
INSERT INTO offers (TripOfferID, TripID, HotelID, SmallRoomsLeft, MediumRoomsLeft, LargeRoomsLeft, ApartmentRoomsLeft,
                    StudioRoomsLeft)
VALUES ('1234', '1', 'OSV', 2, 10, 0, 15, 1);
