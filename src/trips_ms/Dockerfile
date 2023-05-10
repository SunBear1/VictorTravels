FROM eclipse-temurin:17-jdk-alpine as build-stage

WORKDIR /trips

ENV  MONGODB_PORT=27017

ENV  MONGODB_ADDRESS=mongodb

ENV  MONGODB_USER=root

ENV  MONGODB_PASSWORD=student

ENV  MONGODB_DB=rsww_17998_trips_db

COPY .mvn/ .mvn

COPY mvnw pom.xml ./

RUN ./mvnw dependency:resolve

COPY src/ src

RUN ./mvnw package

FROM openjdk:17-jdk-alpine as serve-stage

WORKDIR /trips

COPY --from=build-stage /trips/target/trips-0.0.1-SNAPSHOT.jar ./trips.jar

CMD ["java", "-jar", "trips.jar"]
