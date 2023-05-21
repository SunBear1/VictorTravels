package com.cringe.travels.trips.trip;

import com.cringe.travels.trips.trip.entity.TripConfigurations;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

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
        if (trip == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Trip offer with ID " + id + " does not exist.");
        }
        return ResponseEntity.ok(trip);
    }

    @GetMapping("")
    public ResponseEntity<List<Trip>> getTrips(
            @RequestParam(required = false) Integer adults,
            @RequestParam(required = false) Integer kidsTo3yo,
            @RequestParam(required = false) Integer kidsTo10yo,
            @RequestParam(required = false) Integer kidsTo18yo,
            @RequestParam(required = false) String dateFrom,
            @RequestParam(required = false) String dateTo,
            @RequestParam(required = false) List<String> departureRegion,
            @RequestParam(required = false) List<String> arrivalRegion,
            @RequestParam(required = false) List<String> transport,
            @RequestParam(required = false) String order,
            @RequestParam(required = false) List<String> diet,
            @RequestParam(required = false) Integer maxPrice) {

        List<Trip> trips = service.getFilteredTrips(adults, kidsTo3yo, kidsTo10yo, kidsTo18yo, dateFrom, dateTo, departureRegion, arrivalRegion, transport, order, diet, maxPrice);
        return ResponseEntity.ok(trips);
    }

    @GetMapping("/price")
    @ResponseBody
    ResponseEntity<?> getTripPrice(
            @RequestParam(required = false) Integer adults,
            @RequestParam(required = false) Integer kidsTo3yo,
            @RequestParam(required = false) Integer kidsTo10yo,
            @RequestParam(required = false) Integer kidsTo18yo,
            @RequestParam(required = false) Integer roomCost,
            @RequestParam(required = false) Integer dietCost,
            @RequestParam(required = false) Integer transportToCost,
            @RequestParam(required = false) Integer transportFromCost,
            @RequestParam(required = false) Integer numberOfDays
    ) {
        logger.info("GET REQUEST api/v1/trips/price");
        Float tripPrice = service.calculateTripPrices(adults, kidsTo3yo, kidsTo10yo, kidsTo18yo, roomCost, numberOfDays, transportToCost, transportFromCost, dietCost);
        return ResponseEntity.ok(tripPrice);
    }

    @GetMapping("/configurations")
    @ResponseBody
    ResponseEntity<?> getTripConfigurations() {
        logger.info("GET REQUEST api/v1/trips/configurations");
        TripConfigurations configurations = service.queryForTripConfigurations();
        return ResponseEntity.ok(configurations);
    }
}
