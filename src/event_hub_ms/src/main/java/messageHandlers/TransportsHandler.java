package messageHandlers;

import DTO.TransportEventDTO;
import DTO.TransportGeneratedEventDTO;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.rabbitmq.client.*;
import config.Config;
import database.DatabaseHandler;
import events.RandomGeneratedEvent;
import events.ReservationEvent;
import events.TransportEvent;

import java.io.IOException;
import java.net.ConnectException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.TimeoutException;

public class TransportsHandler implements Runnable {
    private final static String EXCHANGE = "transport-events";
    private final static String ROUTING_KEY = "transport-events-for-transport-ms";
    private final static String QUEUE_NAME_TO_CONSUME = "transport-events-for-eventhub-ms";
    private final DatabaseHandler databaseHandler;
    private ReservationsHandler reservationsMQ;
    private Channel channel;

    public TransportsHandler(DatabaseHandler databaseHandler) {
        this.databaseHandler = databaseHandler;
    }

    public void setReservationsForEventhubMQHandler(ReservationsHandler reservationsMQ) {
        this.reservationsMQ = reservationsMQ;
    }

    @Override
    public void run() {
        ConnectionFactory factory = new ConnectionFactory();
        Config.setConfigFactory(factory);
        try (com.rabbitmq.client.Connection connection = factory.newConnection();
             Channel channel = connection.createChannel()) {

            this.channel = channel;

            DefaultConsumer consumer = new DefaultConsumer(channel) {
                @Override
                public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties,
                                           byte[] body) throws IOException {
                    String message = new String(body, StandardCharsets.UTF_8);
                    System.out.println("[MQ CONSUME] Received message from transportMS queue " + QUEUE_NAME_TO_CONSUME
                            + " with payload: " + message);
                    consumeMessageFromTransport(message);
                    channel.basicAck(envelope.getDeliveryTag(), false);
                }
            };

            channel.basicConsume(QUEUE_NAME_TO_CONSUME, false, consumer);

            while (true) {
                try {
                    Thread.sleep(250);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }

        } catch (ConnectException e) {
            System.err.println("Error: Connection refused. Make sure RabbitMQ is running.");
        } catch (TimeoutException e) {
            System.err.println("Error: Connection timeout occurred.");
            e.printStackTrace();
        } catch (IOException e) {
            System.err.println("Error: I/O exception occurred.");
            e.printStackTrace();
        }
    }

    public void prepareReservationEventMessage(ReservationEvent reservationEvent) {
        String title = "trip_offer_transport_update";
        String trip_offer_id = reservationEvent.getTrip_offer_id();
        String operation_type = (reservationEvent.getReservation_status().equals("created") ? "delete" : "add");
        String connection_id_to = reservationEvent.getConnection_id_to();
        String connection_id_from = reservationEvent.getConnection_id_from();
        int head_count = reservationEvent.getHead_count();

        TransportEventDTO transportEventDTO = new TransportEventDTO(title, trip_offer_id, operation_type, connection_id_to,
                connection_id_from, head_count);
        databaseHandler.saveTransportDTO(transportEventDTO);

        sendMessage(transportEventDTO);
    }

    public void prepareGeneratedEventMessage(RandomGeneratedEvent randomGeneratedEvent){
        String title = "generated_transport_update";
        String connection_id = randomGeneratedEvent.getName();
        String resource_type = randomGeneratedEvent.getResource();
        int value = randomGeneratedEvent.getValue();
        String operation_type = randomGeneratedEvent.getOperation();

        TransportGeneratedEventDTO transportGeneratedEventDTO = new TransportGeneratedEventDTO(title, connection_id, operation_type, value,
                resource_type);
        //databaseHandler.saveHotelDTO(hotelEventDTO);
        sendMessage(transportGeneratedEventDTO);
    }

     public void sendMessage(Object payload){
        ObjectMapper objectMapper = new ObjectMapper();
        try {
            objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
            String json = objectMapper.writeValueAsString(payload);
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
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }
    }
}
