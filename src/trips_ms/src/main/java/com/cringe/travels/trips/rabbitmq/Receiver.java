package com.cringe.travels.trips.rabbitmq;

import java.nio.charset.StandardCharsets;

import com.cringe.travels.trips.trip.TripUpdatesService;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Component
public class Receiver {


    private final TripUpdatesService service;
    Logger logger = LoggerFactory.getLogger(Receiver.class);


    Receiver(TripUpdatesService service) {
        this.service = service;
    }

    public void receiveMessage(byte[] message) {
        String stringMessage = new String(message, StandardCharsets.UTF_8);
        logger.info("GET MESSAGE: " + stringMessage);
        JSONObject jsonObject = new JSONObject(stringMessage);

        String messageTitle = jsonObject.getString("title");

        if (messageTitle.equals(MsgTypes.HOTEL_ROOMS_UPDATE.label)) {
            this.service.updateHotelsRooms(jsonObject);
        } else if (messageTitle.equals(MsgTypes.HOTEL_BOOKINGS_STATUS.label)) {
            this.service.updateTripStatus(jsonObject);
        } else if (messageTitle.equals(MsgTypes.TRANSPORT_UPDATE.label)) {
            this.service.updateTransport(jsonObject);
        } else if (messageTitle.equals(MsgTypes.TRANSPORT_BOOKING_STATUS.label)) {
            this.service.updateTransportStatus(jsonObject);
        }
    }
}
