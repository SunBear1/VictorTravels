package com.cringe.travels.trips;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

import com.cringe.travels.trips.trip.TripRepository;

@EnableMongoRepositories
@SpringBootApplication
public class TripsApplication implements CommandLineRunner {

	@Autowired
    TripRepository tripRepository;
	public static void main(String[] args) {
		SpringApplication.run(TripsApplication.class, args);
	}

	public void run(String... args) {
		Logger logger = LoggerFactory.getLogger(TripsApplication.class);
        logger.info("Trips microservice has been started");
		
	}
}
