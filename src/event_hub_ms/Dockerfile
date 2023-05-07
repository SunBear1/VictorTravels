FROM maven:3.6.3-openjdk-17-slim as build

WORKDIR /event_hub

COPY . .

RUN mvn clean package

CMD ["java", "-jar", "/event_hub/target/eventhub_exec.jar"]
