package com.cringe.travels.trips.trip;

import java.time.LocalDate;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RequestMapping("api/v1/trips")
@RestController
public class TripController {

    private final TripService service;
    Logger logger = LoggerFactory.getLogger(TripController.class);


    TripController(TripService service) {
        this.service = service;
    }

//    @GetMapping("")
//    @ResponseBody
//    List<Trip> getAll() {
//        logger.info("GET REQUEST api/v1/trips");
//        return service.getAllActive();
//    }

    @GetMapping("/{id}")
    @ResponseBody
    ResponseEntity<?> getByOfferId(@PathVariable String id) {
        logger.info("GET REQUEST api/v1/trips/" + id);
        Trip trip = service.getByOfferId(id);
        if(trip == null){
            return ResponseEntity.badRequest().body("Nie ma takiej oferty wycieczki");
        }
        return ResponseEntity.ok(trip);
    }

    @GetMapping("")
    public ResponseEntity<List<Trip>> getTrips(
        @RequestParam(required = false) Integer adults,
        @RequestParam(required = false) Integer kids_to_3yo,
        @RequestParam(required = false) Integer kids_to_10yo,
        @RequestParam(required = false) Integer kids_to_18yo,
        @RequestParam(required = false) LocalDate date_from,
        @RequestParam(required = false) LocalDate date_to,
        @RequestParam(required = false) List<String> departure_region,
        @RequestParam(required = false) List<String> arrival_region,
        @RequestParam(required = false) List<String> transport,
        @RequestParam(required = false) String order,
        @RequestParam(required = false) List<String> diet,
        @RequestParam(required = false) Integer max_price) {
        List<Trip> trips = service.getFilteredTrips(adults, kids_to_3yo, kids_to_10yo, kids_to_18yo, date_from, date_to, departure_region, arrival_region, transport, order, diet, max_price);
    return ResponseEntity.ok(trips);
}
}
