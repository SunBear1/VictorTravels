CREATE TABLE Offers
(
    ID           SERIAL PRIMARY KEY,
    TripOfferID  VARCHAR(50) UNIQUE,
    TripID       VARCHAR(50),
    ConnectionID VARCHAR(50)
);

CREATE TABLE SeatsLeft
(
    ID           SERIAL PRIMARY KEY,
    ConnectionID VARCHAR(50) UNIQUE,
    SeatsLeft    INTEGER
);

INSERT INTO Offers (TripOfferID, TripID, ConnectionID)
VALUES ('1234', '1', 'PRS-WAW-TRAIN-XYZ'),
       ('1235', '2', 'PRS-WAW-TRAIN-XYZ'),
       ('8912', '5', 'ORD-GDN-PLANE-XYZ'),
       ('0921', '3', 'WAW-GDN-PLANE-XYZ');

INSERT INTO SeatsLeft (ConnectionID, SeatsLeft)
VALUES ('PRS-WAW-TRAIN-XYZ', 2),
       ('ORD-GDN-PLANE-XYZ', 14),
       ('WAW-GDN-PLANE-XYZ', 3);
