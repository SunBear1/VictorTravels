package com.cringe.travels.trips.rabbitmq;

public enum MsgTypes {
    HOTEL_ROOMS_UPDATE("hotel_rooms_update"),
    HOTEL_BOOKINGS_STATUS("hotel_booking_status"),
    TRANSPORT_UPDATE("transport_update"),
    TRANSPORT_BOOKING_STATUS("transport_booking_status");

    public final String label;

    private MsgTypes(String label) {
        this.label = label;
    }
}
