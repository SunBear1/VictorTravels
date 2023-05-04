package com.cringe.travels.trips.trip;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

@RequestMapping("api/v1/trips")
@RestController
public class TripController {

    private final TripService service;
    Logger logger = LoggerFactory.getLogger(TripController.class);


    TripController(TripService service){
        this.service = service;
    }

    @GetMapping("")
    @ResponseBody
    List<Trip> getAll() {
        logger.info("GET REQUEST api/v1/trips");
        return service.getAll();
    }

    @GetMapping("/{id}")
    @ResponseBody
    List<Trip> getbyId(@PathVariable String id) {
        logger.info("GET REQUEST api/v1/trips/"+id);
        return service.getbyId(id);
  }
}
