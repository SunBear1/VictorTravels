package com.cringe.travels.trips.trip;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TripController {
    private final TripRepository repository;

    TripController(TripRepository repository){
        this.repository = repository;
    }

    @GetMapping("/trips")
    List<Trip> getAll() {
      return repository.findAll();
    }


  @GetMapping("/trips/{id}")
  List<Trip> getbyId(@PathVariable int id) {
    System.out.println(id);
    return repository.findByTripID(id);
  }
}
