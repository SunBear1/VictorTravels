CREATE TABLE Users (
    id SERIAL PRIMARY KEY ,
    login varchar(255) NOT NULL UNIQUE,
    password varchar(255) NOT NULL
);
