FROM maven:3.6.3-openjdk-17-slim as build-stage

WORKDIR /eventhub

COPY pom.xml ./

COPY src/ src

RUN mvn clean package

FROM openjdk:17-jdk-alpine as serve-stage

WORKDIR /eventhub

RUN apk --no-cache add curl

COPY --from=build-stage /eventhub/target/eventhub_exec.jar ./eventhub.jar

CMD ["java", "-jar", "eventhub.jar"]
