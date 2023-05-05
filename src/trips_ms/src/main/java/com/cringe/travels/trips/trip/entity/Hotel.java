package com.cringe.travels.trips.trip.entity;

import java.util.ArrayList;
import java.util.HashMap;

import org.springframework.data.mongodb.core.mapping.Field;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class Hotel {
    @Field("hotel_id")
    private String hotelId;
    private String name;
    private String image;
    private ArrayList<String> description;
    private HashMap<String, Integer> diet;
    private HashMap<String, RoomDetails> rooms;

}
