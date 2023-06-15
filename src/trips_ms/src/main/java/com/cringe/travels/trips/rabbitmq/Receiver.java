package com.cringe.travels.trips.rabbitmq;

import com.cringe.travels.trips.trip.TripUpdatesService;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import java.nio.charset.StandardCharsets;


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
        } else if (messageTitle.equals(MsgTypes.TRANSPORT_GENERATED_SEATS_UPDATE.label)) {
            this.service.updateGeneratedTransportSeats(jsonObject);
        } else if (messageTitle.equals(MsgTypes.TRANSPORT_GENERATED_PRICE_UPDATE.label)) {
            this.service.updateGeneratedTransportPrice(jsonObject);
        } else if (messageTitle.equals(MsgTypes.HOTEL_PRICE_UPDATE.label)) {
            this.service.updateHotelPrice(jsonObject);
        } else {
            logger.info("Unknown message type");
        }
    }
}
