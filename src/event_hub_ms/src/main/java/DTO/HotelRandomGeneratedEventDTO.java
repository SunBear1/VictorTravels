package DTO;

public class HotelRandomGeneratedEventDTO {
    private final String title;
    private final String operation;
    private final String hotel_id;
    private final String room_type;
    private final String resource_type;
    private final int resource_amount;

    public HotelRandomGeneratedEventDTO(String title, String operation, String hotel_id,
            String room_type, String resource_type, int resource_amount) {
        this.title = title;
        this.operation = operation;
        this.hotel_id = hotel_id;
        this.room_type = room_type;
        this.resource_amount = resource_amount;
        this.resource_type = resource_type;
    }

    public String getTitle() {
        return title;
    }

    public String getOperation() {
        return operation;
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
