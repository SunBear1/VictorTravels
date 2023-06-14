package messageHandlers;

import DTO.ReservationDTO;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.rabbitmq.client.*;
import config.Config;
import database.DatabaseHandler;
import events.HotelEvent;
import events.ReservationEvent;
import events.TransportEvent;

import java.io.IOException;
import java.net.ConnectException;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.concurrent.TimeoutException;

public class ReservationsHandler implements Runnable {
    private final static String EXCHANGE = "reservations";
    private final static String ROUTING_KEY = "reservations-for-reservations-ms";
    private final static String QUEUE_NAME_TO_CONSUME = "reservations-for-eventhub-ms";
    private final DatabaseHandler databaseHandler;
    private Channel channel;
    private final HotelsHandler hotelMQ;
    private final TransportsHandler transportMQ;
    private final LiveEventsHandler liveEventsMQ;

    public ReservationsHandler(DatabaseHandler databaseHandler, HotelsHandler hotelMQ,
                               TransportsHandler transportMQ, LiveEventsHandler liveEventsMQ) {
        this.databaseHandler = databaseHandler;
        this.transportMQ = transportMQ;
        this.hotelMQ = hotelMQ;
        this.liveEventsMQ = liveEventsMQ;
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
                    System.out.println("[MQ CONSUME] Received message from reservationMS queue " + QUEUE_NAME_TO_CONSUME
                            + " with payload: " + message);
                    consumeMessageFromReservations(message);
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

    public void consumeMessageFromReservations(String json) {
        try {
            ObjectMapper mapper = new ObjectMapper();
            ReservationEvent reservationEvent = mapper.readValue(json, ReservationEvent.class);
            databaseHandler.saveReservationEvent(reservationEvent);

            if (!reservationEvent.getReservation_status().equals("finalize")) {
                if (!reservationEvent.getReservation_status().equals("created")) {
                    ReservationEvent tmp = databaseHandler.getReservationById(reservationEvent.getReservation_id());

                    reservationEvent.setHotel_id(tmp.getHotel_id());
                    reservationEvent.setRoom_type(tmp.getRoom_type());
                    reservationEvent.setConnection_id_to(tmp.getConnection_id_to());
                    reservationEvent.setConnection_id_from(tmp.getConnection_id_from());
                    reservationEvent.setHead_count(tmp.getHead_count());
                }
                hotelMQ.prepareReservationEventMessage(reservationEvent);
                transportMQ.prepareReservationEventMessage(reservationEvent);
            }

            if (reservationEvent.getReservation_status().equals("created")
                    || reservationEvent.getReservation_status().equals("finalized")) {
                liveEventsMQ.sendReservationEventMessage(reservationEvent);
            }
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }
    }

    public void sendMessageFromHotel(HotelEvent hotelEvent) {
        String title = hotelEvent.getTitle();
        List<String> trip_offers_affected = hotelEvent.getTrip_offers_id();
        String operation_type = (hotelEvent.getIs_hotel_booked_up() ? "delete" : "add");

        ReservationDTO reservationDTO = new ReservationDTO(title, operation_type, trip_offers_affected, null);
        databaseHandler.saveReservationDTO(reservationDTO);
        ObjectMapper objectMapper = new ObjectMapper();
        try {
            objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
            String json = objectMapper.writeValueAsString(reservationDTO);
            channel.basicPublish(EXCHANGE, ROUTING_KEY, null, json.getBytes());
            System.out.println("[MQ PUBLISH] Published hotel message to reservationMS exchange " +
                    ROUTING_KEY + " with payload: " + json);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void sendMessageFromTransport(TransportEvent transportEvent) {
        String title = transportEvent.getTitle();
        List<String> trip_offers_affected = transportEvent.getTrip_offers_id();
        String operation_type = (transportEvent.getIs_transport_booked_up() ? "delete" : "add");
        String connection_id = transportEvent.getConnection_id();

        ReservationDTO reservationDTO = new ReservationDTO(title, operation_type, trip_offers_affected, connection_id);
        databaseHandler.saveReservationDTO(reservationDTO);
        ObjectMapper objectMapper = new ObjectMapper();
        try {
            objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
            String json = objectMapper.writeValueAsString(reservationDTO);
            channel.basicPublish(EXCHANGE, ROUTING_KEY, null, json.getBytes());
            System.out.println("[MQ PUBLISH] Published transport message to reservationMS exchange " +
                    ROUTING_KEY + " with payload: " + json);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
