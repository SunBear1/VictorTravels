CREATE TABLE Trips
(
    id   SERIAL PRIMARY KEY,
    type varchar(255) NOT NULL,
    body varchar(255) NOT NULL
);