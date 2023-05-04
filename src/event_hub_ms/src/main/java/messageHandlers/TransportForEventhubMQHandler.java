package messageHandlers;
import DTO.TransportDTO;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.rabbitmq.client.*;
import config.Config;
import database.DatabaseHandler;
import events.ReservationEvent;
import events.TransportEvent;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class TransportForEventhubMQHandler implements Runnable{
    private final static String EXCHANGE = "transport-events";
    private final static String ROUTING_KEY = "transport-events-for-transport-ms";
    private final static String QUEUE_NAME_TO_CONSUME = "transport-events-for-eventhub-ms";
    private final DatabaseHandler databaseHandler;
    private ReservationsForEventhubMQHandler reservationsMQ;
    private Channel channel;

    public TransportForEventhubMQHandler(DatabaseHandler databaseHandler) {
        this.databaseHandler = databaseHandler;
    }

    public void setReservationsForEventhubMQHandler(ReservationsForEventhubMQHandler reservationsMQ) {
        this.reservationsMQ = reservationsMQ;
    }

    @Override
    public void run() {
        System.out.println("Hello from transport thread!");

        ConnectionFactory factory = new ConnectionFactory();
        Config.setConfigFactory(factory);
        try (com.rabbitmq.client.Connection connection = factory.newConnection();
             Channel channel = connection.createChannel()) {

            this.channel = channel;

            DefaultConsumer consumer = new DefaultConsumer(channel) {
                @Override
                public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {
                    String message = new String(body, "UTF-8");
                    System.out.println("[MQ CONSUME] Received message from transportMS queue " + QUEUE_NAME_TO_CONSUME + " with payload: " + message);
                    consumeMessageFromTransport(message);
                    channel.basicAck(envelope.getDeliveryTag(), false);
                }
            };

            channel.basicConsume(QUEUE_NAME_TO_CONSUME, false, consumer);

            while (true) {
                ;
            }

        } catch (TimeoutException | IOException e) {
            e.printStackTrace();
        }
    }

    public void sendMessage(ReservationEvent reservationEvent) {
        String title = "trip_offer_transport_update";
        String trip_offer_id = reservationEvent.getTrip_offer_id();
        String operation_type = (reservationEvent.getReservation_status().equals("created") ? "delete" : "add");
        String connection_id = reservationEvent.getConnection_id();

        TransportDTO transportDTO = new TransportDTO(title, trip_offer_id, operation_type, connection_id);
        databaseHandler.saveTransportDTO(transportDTO);

        ObjectMapper objectMapper = new ObjectMapper();
        try {
            objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
            String json = objectMapper.writeValueAsString(transportDTO);
            channel.basicPublish(EXCHANGE, ROUTING_KEY, null, json.getBytes());
            System.out.println("[MQ PUBLISH] Published message to transportMS exchange " +
                    ROUTING_KEY + " with payload: " + json);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void consumeMessageFromTransport(String json) {
        try {
            ObjectMapper mapper = new ObjectMapper();
            TransportEvent transportEvent = mapper.readValue(json, TransportEvent.class);
            databaseHandler.saveTransportEvent(transportEvent);

            reservationsMQ.sendMessageFromTransport(transportEvent);
        }
        catch (JsonProcessingException e) {
            e.printStackTrace();
        }
    }
}
