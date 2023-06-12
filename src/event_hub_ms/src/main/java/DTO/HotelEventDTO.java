package DTO;

public class HotelEventDTO {
    private final String title;
    private final String trip_offer_id;
    private final String operation_type;
    private final String hotel_id;
    private final String room_type;
    private final int resource_amount;
    private final String resource_type;

    public HotelEventDTO(String title, String trip_offer_id, String operation_type, String hotel_id,
                         String room_type, int resource_amount, String resource_type) {
        this.title = title;
        this.trip_offer_id = trip_offer_id;
        this.operation_type = operation_type;
        this.hotel_id = hotel_id;
        this.room_type = room_type;
        this.resource_amount = resource_amount;
        this.resource_type = resource_type;
    }

    public String getTitle() {
        return title;
    }

    public String getTrip_offer_id() {
        return trip_offer_id;
    }

    public String getOperation_type() {
        return operation_type;
    }

    public String getHotel_id() {
        return hotel_id;
    }

    public String getRoom_type() {
        return room_type;
    }

    public int getResource_amount() {
        return resource_amount;
    }

    public String getResource_type() {
        return resource_type;
    }
}
