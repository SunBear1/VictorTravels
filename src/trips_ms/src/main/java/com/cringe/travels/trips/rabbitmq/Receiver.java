package com.cringe.travels.trips.rabbitmq;

import java.nio.charset.StandardCharsets;

import org.json.JSONObject;
import org.springframework.stereotype.Component;

import com.cringe.travels.trips.trip.TripService;

@Component
public class Receiver {


    private final TripService service;

    Receiver(TripService service){
        this.service = service;
    }

    public void receiveMessage(byte[] message) {
        String stringMessage = new String(message, StandardCharsets.UTF_8);
        JSONObject jsonObject = new JSONObject(stringMessage);

        String messageTitle = jsonObject.getString("title");

        if (messageTitle.equals(MsgTypes.HOTEL_ROOMS_UPDATE.label)){
          this.service.updateHotelsRooms(jsonObject);
        }
      }
}
