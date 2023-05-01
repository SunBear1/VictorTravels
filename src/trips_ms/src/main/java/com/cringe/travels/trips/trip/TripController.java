package com.cringe.travels.trips.trip;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TripController {

    private final TripService service;

    TripController(TripService service){
        this.service = service;
    }

    @GetMapping("/trips")
    List<Trip> getAll() {
      return service.getAll();
    }


    @GetMapping("/trips/{id}")
    List<Trip> getbyId(@PathVariable int id) {
      System.out.println(id);
      return service.getbyId(id);
  }
}
