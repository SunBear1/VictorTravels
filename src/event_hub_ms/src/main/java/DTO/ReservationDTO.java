package DTO;

import java.util.List;

public class ReservationDTO {
    private String title;
    private String operation_type;
    private List<String> trip_offers_affected;
    private String connection_id;

    public ReservationDTO(String title, String operation_type, List<String> trip_offers_affected, String connection_id) {
        this.title = title;
        this.operation_type = operation_type;
        this.trip_offers_affected = trip_offers_affected;
        this.connection_id = connection_id;
    }

    public String getTitle() {
        return title;
    }

    public String getOperation_type() {
        return operation_type;
    }

    public List<String> getTrip_offers_affected() {
        return trip_offers_affected;
    }

    public String getConnection_id() {
        return connection_id;
    }
}
