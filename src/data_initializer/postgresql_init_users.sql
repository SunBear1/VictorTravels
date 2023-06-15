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

CREATE TABLE GeneratedEvents
(
    id        INTEGER PRIMARY KEY,
    title     varchar(255) NOT NULL,
    type      varchar(255) NOT NULL,
    name      varchar(255) NOT NULL,
    field     varchar(255) NOT NULL,
    resource  varchar(255) NOT NULL,
    value     INTEGER      NOT NULL,
    operation varchar(255) NOT NULL
);
