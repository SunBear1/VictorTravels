package com.cringe.travels.trips.rabbitmq;

public enum MsgTypes {
    HOTEL_ROOMS_UPDATE("hotel_rooms_availability_update"),
    HOTEL_PRICE_UPDATE("hotel_room_price_update"),
    HOTEL_BOOKINGS_STATUS("hotel_booking_status"),
    TRANSPORT_UPDATE("transport_update"),
    TRANSPORT_BOOKING_STATUS("transport_booking_status"),
    TRANSPORT_GENERATED_SEATS_UPDATE("generated_transport_availability_update"),
    TRANSPORT_GENERATED_PRICE_UPDATE("generated_transport_price_update");

    public final String label;

    MsgTypes(String label) {
        this.label = label;
    }
}
