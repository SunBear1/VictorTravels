package events;

public class ReservationEvent {
    private String title;
    private Integer trip_offer_id;
    private String reservation_id;
    private String reservation_status;
    private String hotel_id;
    private String room_type;
    private String connection_id;

    public String getTitle() {
        return title;
    }

    public Integer getTrip_offer_id() {
        return trip_offer_id;
    }

    public String getReservation_id() {
        return reservation_id;
    }

    public String getReservation_status() {
        return reservation_status;
    }

    public String getHotel_id() {
        return hotel_id;
    }

    public String getRoom_type() {
        return room_type;
    }

    public String getConnection_id() {
        return connection_id;
    }

    public void setHotel_id(String hotel_id) {
        this.hotel_id = hotel_id;
    }

    public void setRoom_type(String room_type) {
        this.room_type = room_type;
    }

    public void setConnection_id(String connection_id) {
        this.connection_id = connection_id;
    }
}
