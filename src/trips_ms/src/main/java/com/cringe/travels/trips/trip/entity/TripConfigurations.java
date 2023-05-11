package com.cringe.travels.trips.trip.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import java.util.List;

@Data
@AllArgsConstructor
public class TripConfigurations {
    private List<String> departureLocations;
    private List<Localisation> arrivalLocations;
    private List<String> transportTypes;
}
