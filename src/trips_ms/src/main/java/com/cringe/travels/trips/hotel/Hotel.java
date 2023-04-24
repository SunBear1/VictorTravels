package com.cringe.travels.trips.hotel;

import java.util.ArrayList;
import java.util.HashMap;


import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class Hotel {
    String name;
    String image;
    ArrayList<String> description;
    HashMap<String,Integer> diet;
}
