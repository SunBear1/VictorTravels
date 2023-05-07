FROM eclipse-temurin:17-jdk-jammy

WORKDIR /trips

RUN apt-get update && apt-get install dos2unix

COPY .mvn/ .mvn

COPY mvnw pom.xml ./

RUN dos2unix mvnw

RUN ./mvnw dependency:resolve

COPY src ./src

CMD ["./mvnw", "spring-boot:run"]
