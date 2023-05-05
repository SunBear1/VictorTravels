package events;

import java.util.List;

public class TransportEvent {
    private String title;
    private List<String> trip_offers_id;
    private String connection_id_to;
    private String connection_id_from;
    private Boolean is_transport_booked_up;

    public TransportEvent() {
    }

    public String getTitle() {
        return title;
    }

    public List<String> getTrip_offers_id() {
        return trip_offers_id;
    }

    public String getConnection_id_to() {
        return connection_id_to;
    }

    public String getConnection_id_from() {
        return connection_id_from;
    }

    public Boolean getIs_transport_booked_up() {
        return is_transport_booked_up;
    }
}
