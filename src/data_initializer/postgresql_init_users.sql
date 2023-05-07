CREATE TABLE Users
(
    ID       SERIAL PRIMARY KEY,
    login    varchar(255) NOT NULL UNIQUE,
    password varchar(255) NOT NULL
);
INSERT INTO Users (login, password)
VALUES ('example_user@example.com', 'example_password'),
       ('wiktor@interia.pl', 'bigv123'),
       ('admin@wp.pl', 'admin');
