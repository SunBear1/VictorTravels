package DTO;

public class TransportDTO {
    private String title;
    private Integer trip_offer_id;
    private String operation_type;
    private String connection_id;

    public TransportDTO(String title, Integer trip_offer_id, String operation_type, String connection_id) {
        this.title = title;
        this.trip_offer_id = trip_offer_id;
        this.operation_type = operation_type;
        this.connection_id = connection_id;
    }

    public String getTitle() {
        return title;
    }

    public Integer getTrip_offer_id() {
        return trip_offer_id;
    }

    public String getOperation_type() {
        return operation_type;
    }

    public String getConnection_id() {
        return connection_id;
    }
}
