CREATE TABLE Users (
    id SERIAL PRIMARY KEY ,
    login varchar(255) NOT NULL UNIQUE,
    password varchar(255) NOT NULL
);

CREATE TABLE Hotels (
    ID SERIAL PRIMARY KEY,
    Name TEXT,
    LocationID INTEGER
);

CREATE TABLE RoomTypes (
    ID SERIAL PRIMARY KEY,
    Name TEXT,
    Capacity INTEGER,
    BaseCost INTEGER
);

CREATE TABLE HotelDiet (
    ID SERIAL PRIMARY KEY,
    HotelID INTEGER,
    MealTypeID INTEGER,
    Cost INTEGER
);

CREATE TABLE MealTypes (
    ID SERIAL PRIMARY KEY,
    MealType TEXT
);

CREATE TABLE Rooms (
    ID SERIAL PRIMARY KEY,
    HotelID INTEGER,
    RoomTypeID INTEGER
);

CREATE TABLE Bookings (
    ID SERIAL PRIMARY KEY,
    ReservationID INTEGER,
    RoomID INTEGER,
    CheckInDate DATE,
    CheckOutDate DATE
);

CREATE TABLE Transport (
    ID SERIAL PRIMARY KEY,
    FromCity TEXT,
    ToCity TEXT,
    Kind TEXT,
    Capacity INTEGER,
    Cost INTEGER
);

CREATE TABLE TimeTable (
    ID SERIAL PRIMARY KEY,
    ReservationID INTEGER,
    TransportID INTEGER,
    DepartureTime TIMESTAMP,
    ArrivalTime TIMESTAMP,
    SeatsBooked INTEGER
);

