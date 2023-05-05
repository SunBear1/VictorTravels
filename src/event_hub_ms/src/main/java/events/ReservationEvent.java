package events;

public class ReservationEvent {
    private String title;
    private String trip_offer_id;
    private String reservation_id;
    private String reservation_status;
    private String hotel_id;
    private String room_type;
    private String connection_id_to;
    private String connection_id_from;
    private int head_count;

    public ReservationEvent() {
    }

    public String getTitle() {
        return title;
    }

    public String getTrip_offer_id() {
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

    public String getConnection_id_to() {
        return connection_id_to;
    }

    public String getConnection_id_from() {
        return connection_id_from;
    }

    public int getHead_count() {
        return head_count;
    }

    public void setHotel_id(String hotel_id) {
        this.hotel_id = hotel_id;
    }

    public void setRoom_type(String room_type) {
        this.room_type = room_type;
    }

    public void setConnection_id_to(String connection_id_to) {
        this.connection_id_to = connection_id_to;
    }

    public void setConnection_id_from(String connection_id_from) {
        this.connection_id_from = connection_id_from;
    }

    public void setHead_count(int head_count) {
        this.head_count = head_count;
    }
}
