package com.cringe.travels.trips.trip;

import java.util.List;

public class TripService {

    private final TripRepository repository;

    TripService(TripRepository repository){
        this.repository = repository;
    }

    List<Trip> getAll() {
      return repository.findAll();
    }


    List<Trip> getbyId(int id) {
      System.out.println(id);
      return repository.findByTripID(id);
  }
}
