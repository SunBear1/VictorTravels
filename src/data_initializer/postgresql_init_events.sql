CREATE TABLE EventsLog
(
    ID          SERIAL PRIMARY KEY,
    Type        varchar(50),
    Operation   varchar(50),
    "From"      varchar(50),
    "To"        varchar(50),
    ReceiveDate timestamp,
    Body        json
);

CREATE TABLE TripsForLiveEvents
(
    OfferID   VARCHAR(50) PRIMARY KEY,
    TripID    INTEGER,
    HotelID   VARCHAR(20),
    HotelName VARCHAR(50),
    Country   VARCHAR(30),
    Region    VARCHAR(30)
);

INSERT INTO TripsForLiveEvents (OfferID, TripID, HotelID, HotelName, Country, Region)
VALUES ('0001', 1, 'HFP-1', 'Hotel Fuerteventura Princess', 'Wyspy Kanaryjskie', 'Fuerteventura'),
       ('0002', 2, 'HAB-1', 'Hotel Alhambra', 'Hiszpania', 'Costa Brava'),
       ('0003', 3, 'HGR-1', 'Hotel Gaia Royal', 'Grecja', 'Kos'),
       ('0004', 4, 'HSMKB-1', 'Hotel Smy Kos Beach & Splash', 'Grecja', 'Kos'),
       ('0005', 5, 'HHINER-1', 'Hotel Holiday Inn Express Rzeszów Airport', 'Polska', 'Rzeszów'),
       ('0006', 5, 'HHINER-2', 'Hotel Holiday Inn Express Rzeszów Airport', 'Polska', 'Rzeszów');
