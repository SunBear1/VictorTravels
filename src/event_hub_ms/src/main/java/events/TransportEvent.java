package events;

import java.util.List;

public class TransportEvent {
    private String title;
    private List<String> trip_offers_id;
    private String connection_id;
    private Boolean is_transport_booked_up;

    public TransportEvent() {
    }

    public String getTitle() {
        return title;
    }

    public List<String> getTrip_offers_id() {
        return trip_offers_id;
    }

    public String getConnection_id() {
        return connection_id;
    }

    public Boolean getIs_transport_booked_up() {
        return is_transport_booked_up;
    }
}
