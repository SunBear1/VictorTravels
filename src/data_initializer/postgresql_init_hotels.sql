CREATE TABLE Offers
(
    id          SERIAL PRIMARY KEY,
    TripOfferID VARCHAR(50) UNIQUE,
    TripID      VARCHAR(50),
    HotelID     VARCHAR(50)
);

INSERT INTO Offers (TripOfferID, TripID, HotelID)
VALUES ('1234', '1', 'OSV-XYZ'),
       ('4212', '2', 'OSV-XYZ'),
       ('9124', '3', 'BTV-XYZ'),
       ('1235', '1', 'OSV-TCV');

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
VALUES ('OSV-XYZ', 2, 10, 0, 15, 1),
       ('OSV-TCV', 0, 2, 6, 3, 0),
       ('BTV-XYZ', 5, 1, 2, 0, 2);

