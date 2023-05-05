package com.cringe.travels.trips.trip;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

public interface TripRepository extends MongoRepository<Trip, String> {

    List<Trip> findAll();

    @Query("{ 'trip_id' : ?0 }")
    Trip findByTripID(String tripID);

    @Query("{ 'is_booked_up' : false }")
    List<Trip> findAllActiveTrips();

}
