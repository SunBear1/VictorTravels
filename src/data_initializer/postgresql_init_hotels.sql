CREATE TABLE Offers
(
    ID          SERIAL PRIMARY KEY,
    TripOfferID VARCHAR(50) UNIQUE,
    TripID      VARCHAR(50),
    HotelID     VARCHAR(50)
);

INSERT INTO Offers (TripOfferID, TripID, HotelID)
VALUES ('0001', '1', 'HFP-1'),
       ('0002', '2', 'HAB-1'),
       ('0003', '3', 'HGR-1'),
       ('0004', '4', 'HSMKB-1'),
       ('0005', '5', 'HHINER-1'),
       ('0006', '5', 'HHINER-2');

CREATE TABLE RoomsLeft
(
    ID                 SERIAL PRIMARY KEY,
    HotelID            VARCHAR(50) UNIQUE,
    SmallRoomsLeft     INTEGER,
    MediumRoomsLeft    INTEGER,
    LargeRoomsLeft     INTEGER,
    ApartmentRoomsLeft INTEGER,
    StudioRoomsLeft    INTEGER
);

INSERT INTO RoomsLeft (HotelID, SmallRoomsLeft, MediumRoomsLeft, LargeRoomsLeft, ApartmentRoomsLeft, StudioRoomsLeft)
VALUES ('HHINER-2', 12, 6, 10, 3, 1),
       ('HHINER-1', 12, 6, 10, 3, 1),
       ('HSMKB-1', 15, 5, 0, 2, 5),
       ('HGR-1', 2, 10, 20, 0, 0),
       ('HAB-1', 3, 9, 20, 5, 15),
       ('HFP-1', 20, 1, 3, 0, 1);

