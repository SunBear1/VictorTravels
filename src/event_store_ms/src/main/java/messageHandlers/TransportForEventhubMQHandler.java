package messageHandlers;
import DTO.TransportDTO;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.rabbitmq.client.*;
import config.Config;
import database.DatabaseHandler;
import events.ReservationEvent;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class TransportForEventhubMQHandler {
    private final static String QUEUE_NAME = "transport-events-for-eventhub-ms";
    private final DatabaseHandler databaseHandler;
    private Channel channel;

    public TransportForEventhubMQHandler(DatabaseHandler databaseHandler) {
        this.databaseHandler = databaseHandler;
    }

    public void setup() {
        System.out.println("Hello from thread " + QUEUE_NAME);

        ConnectionFactory factory = new ConnectionFactory();
        Config.setConfigFactory(factory);
        Connection connection = null;
        try {
            connection = factory.newConnection();
            channel = connection.createChannel();
        } catch (IOException | TimeoutException e) {
            e.printStackTrace();
        }
    }

    public void processMessage(ReservationEvent reservationEvent) {
        System.out.println("Some operations for " + QUEUE_NAME + "...");

        String title = "trip_offer_transport_update";
        Integer trip_offer_id = reservationEvent.getTrip_offer_id();
        String operation_type = (reservationEvent.getReservation_status().equals("created") ? "add" : "delete");
        String connection_id = reservationEvent.getConnection_id();

        TransportDTO transportDTO = new TransportDTO(title, trip_offer_id, operation_type, connection_id);
        databaseHandler.saveTransportDTO(transportDTO);

        ObjectMapper objectMapper = new ObjectMapper();
        try {
            String json = objectMapper.writeValueAsString(transportDTO);
            channel.basicPublish("", QUEUE_NAME, null, json.getBytes());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
