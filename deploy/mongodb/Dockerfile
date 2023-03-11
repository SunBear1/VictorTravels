FROM mongo:6.0 as build-stage

WORKDIR /db

ENV MONGO_INITDB_ROOT_USERNAME=admin

ENV MONGO_INITDB_ROOT_PASSWORD=admin

COPY init.js /docker-entrypoint-initdb.d

EXPOSE 27017
