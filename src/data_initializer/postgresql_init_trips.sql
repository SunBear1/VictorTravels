CREATE TABLE Trips
(
    id   SERIAL PRIMARY KEY,
    name varchar(255) NOT NULL UNIQUE
);