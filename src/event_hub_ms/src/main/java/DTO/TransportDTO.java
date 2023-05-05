package DTO;

public class TransportDTO {
    private String title;
    private String trip_offer_id;
    private String operation_type;
    private String connection_id;
    private int head_count;

    public TransportDTO(String title, String trip_offer_id, String operation_type, String connection_id, int head_count) {
        this.title = title;
        this.trip_offer_id = trip_offer_id;
        this.operation_type = operation_type;
        this.connection_id = connection_id;
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

    public String getConnection_id() {
        return connection_id;
    }

    public int getHead_count(){
        return head_count;
    }
}
