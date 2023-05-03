package DTO;

import java.util.List;

public class ReservationDTO {
    private String title;
    private String operation_type;
    private List<String> trip_offers_affected;
    private List<String> connection_affected;

    public ReservationDTO(String title, String operation_type, List<String> trip_offers_affected, List<String> connection_affected){
        this.title = title;
        this.operation_type = operation_type;
        this.trip_offers_affected = trip_offers_affected;
        this.connection_affected = connection_affected;
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

    public List<String> getConnection_affected() {
        return connection_affected;
    }
}
