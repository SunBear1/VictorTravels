package com.cringe.travels.trips.trip;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TripController {

    private final TripService service;
    Logger logger = LoggerFactory.getLogger(TripController.class);


    TripController(TripService service){
        this.service = service;
    }

    @GetMapping("/trips")
    List<Trip> getAll() {
        logger.info("GET REQUEST /trips");
        return service.getAll();
    }


    @GetMapping("/trips/{id}")
    List<Trip> getbyId(@PathVariable String id) {
        logger.info("GET REQUEST /trips/"+id);
        return service.getbyId(id);
  }
}
