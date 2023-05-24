package DTO;

public class LiveEventsDTO {
    private static final String title = "live_events_generation";
    private final Integer trip_id;
    private final String country;
    private String region;
    private final String hotel_name;
    private String room_type;
    private String transport_type;

    public LiveEventsDTO(Integer trip_id, String country, String region, String hotel_name, String room_type,
                         String transport_type) {
        this.trip_id = trip_id;
        this.country = region;
        this.hotel_name = hotel_name;
        this.room_type = room_type;
        this.transport_type = transport_type;
    }

    public String getTitle() {
        return LiveEventsDTO.title;
    }

    public String getCountry() {
        return this.country;
    }

    public String getRegion() {
        return this.region;
    }

    public Integer getTripID() {
        return this.trip_id;
    }

    public String getHotelName() {
        return this.hotel_name;
    }

    public String getRoomType() {
        return this.room_type;
    }

    public String getTransportType() {
        return this.transport_type;
    }

    public void setTransportType(String transport_type) {
        this.transport_type = transport_type;
    }

    public void setRoomType(String room_type) {
        this.room_type = room_type;
    }

}
