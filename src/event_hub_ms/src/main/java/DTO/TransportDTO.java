package DTO;

public class TransportDTO {
    private final String title;
    private final String trip_offer_id;
    private final String operation_type;
    private final String connection_id_to;
    private final String connection_id_from;
    private final int head_count;

    public TransportDTO(String title, String trip_offer_id, String operation_type, String connection_id_to, String connection_id_from, int head_count) {
        this.title = title;
        this.trip_offer_id = trip_offer_id;
        this.operation_type = operation_type;
        this.connection_id_to = connection_id_to;
        this.connection_id_from = connection_id_from;
        this.head_count = head_count;
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

    public String getConnection_id_to() {
        return connection_id_to;
    }

    public String getConnection_id_from() {
        return connection_id_from;
    }

    public int getHead_count() {
        return head_count;
    }
}
