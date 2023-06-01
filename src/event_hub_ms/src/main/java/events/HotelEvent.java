package events;

import java.util.List;

public class HotelEvent {
    private String title;
    private List<String> trip_offers_id;
    private Boolean is_hotel_booked_up;

    public HotelEvent() {
    }

    public String getTitle() {
        return title;
    }

    public List<String> getTrip_offers_id() {
        return trip_offers_id;
    }

    public Boolean getIs_hotel_booked_up() {
        return is_hotel_booked_up;
    }
}
