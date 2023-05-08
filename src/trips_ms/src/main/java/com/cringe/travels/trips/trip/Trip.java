package com.cringe.travels.trips.trip;

import java.util.HashMap;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import com.cringe.travels.trips.trip.entity.Hotel;
import com.cringe.travels.trips.trip.entity.Localisation;
import com.cringe.travels.trips.trip.entity.Transport;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
@Document("trips")
public class Trip {
    @Id
    private String id;

    @Field("trip_id")
    private String tripID;

    @Field("is_booked_up")
    private boolean bookedUp;

    @Field("date_from")
    private String dateFrom;

    @Field("date_to")
    private String dateTo;

    private Hotel hotel;

    private Localisation localisation;

    private HashMap<String, Transport> from;

    private HashMap<String, Transport> to;
}
