package DTO;

public class TransportGeneratedEventDTO {
    private final String title;
    private final String connection_id;
    private final String operation_type;
    private final int value;
    private final String resource_type;

    public TransportGeneratedEventDTO(String title, String connection_id, String operation_type, int value, String resource_type) {
        this.title = title;
        this.connection_id = connection_id;
        this.operation_type = operation_type;
        this.value = value;
        this.resource_type = resource_type;
    }

    public String getTitle() {
        return title;
    }

    public String getConnection_id() {
        return connection_id;
    }

    public String getOperation_type() {
        return operation_type;
    }

    public int getValue() {
        return value;
    }

    public String getResource_type() {
        return resource_type;
    }


}
