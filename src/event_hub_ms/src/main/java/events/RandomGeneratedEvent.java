package events;

public class RandomGeneratedEvent {
    String title;
    String type;
    String name;
    String field;
    String resource;
    int value;
    String operation;
    int id;

    public String getTitle() {
        return title;
    }

    public String getType() {
        return type;
    }

    public String getName() {
        return name;
    }

    public String getField() {
        return field;
    }

    public String getResource() {
        return resource;
    }

    public int getId() {
        return id;
    }

    public String getOperation() {
        return operation;
    }

    public int getValue() {
        return value;
    }

    public void setField(String field) {
        this.field = field;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setOperation(String operation) {
        this.operation = operation;
    }

    public void setResource(String resource) {
        this.resource = resource;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public void setType(String type) {
        this.type = type;
    }

    public void setValue(int value) {
        this.value = value;
    }
}
