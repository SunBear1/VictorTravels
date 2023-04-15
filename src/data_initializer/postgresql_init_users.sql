CREATE TABLE Userss
(
    id       SERIAL PRIMARY KEY,
    login    varchar(255) NOT NULL UNIQUE,
    password varchar(255) NOT NULL
);
INSERT INTO Userss (login, password)
VALUES ('example_user', 'example_password');
