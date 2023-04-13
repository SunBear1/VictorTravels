FROM postgres:alpine as build-stage

WORKDIR /db

COPY init.sql /docker-entrypoint-initdb.d

ENV POSTGRES_USER=admin

ENV POSTGRES_PASSWORD=admin

ENV POSTGRES_DB=users

EXPOSE 5432
