package messageHandlers;
import DTO.TransportDTO;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.rabbitmq.client.*;
import config.Config;
import database.DatabaseHandler;
import events.HotelEvent;
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
                    System.out.println(" [x] Received '" + message + "'" + " from " + QUEUE_NAME_TO_CONSUME);
                    processMessage(message);
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
        System.out.println("Message to produce in " + ROUTING_KEY + " by transport from reservations...");

        String title = "trip_offer_transport_update";
        String trip_offer_id = reservationEvent.getTrip_offer_id();
        String operation_type = (reservationEvent.getReservation_status().equals("created") ? "add" : "delete");
        String connection_id = reservationEvent.getConnection_id();

        TransportDTO transportDTO = new TransportDTO(title, trip_offer_id, operation_type, connection_id);
        databaseHandler.saveTransportDTO(transportDTO);

        ObjectMapper objectMapper = new ObjectMapper();
        try {
            String json = objectMapper.writeValueAsString(transportDTO);
            channel.basicPublish(EXCHANGE, ROUTING_KEY, null, json.getBytes());
            System.out.println("Message " + json + " to " + ROUTING_KEY + " published!");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void processMessage(String json) {
        try {
            System.out.println("Message from " + QUEUE_NAME_TO_CONSUME + " to consume by transport...");
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
