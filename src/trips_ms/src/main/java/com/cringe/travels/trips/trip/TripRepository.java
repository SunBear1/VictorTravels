package com.cringe.travels.trips.trip;

import java.util.List;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

public interface TripRepository extends MongoRepository<Trip, String>  {
   
    List<Trip> findAll();

    @Query("{ 'tripID' : ?0 }")
    List<Trip> findByTripID(int tripID);

}
