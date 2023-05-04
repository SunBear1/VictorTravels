package com.cringe.travels.trips.trip.entity;

import org.springframework.data.mongodb.core.mapping.Field;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class TransportDetails {
    @Field("id")
    private String id;
    private int cost;
    private int seatsLeft;
}
