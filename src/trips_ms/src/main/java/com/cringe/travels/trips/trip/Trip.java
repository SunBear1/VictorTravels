package com.cringe.travels.trips.trip;

import org.bson.types.ObjectId;
import org.springframework.data.mongodb.core.mapping.Document;

import com.cringe.travels.trips.hotel.Hotel;
import com.cringe.travels.trips.localisation.Localisation;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
@Document("trips")
public class Trip {
    private ObjectId id;
    private int tripID;
    private Hotel hotel;
    private Localisation localisation;
}
