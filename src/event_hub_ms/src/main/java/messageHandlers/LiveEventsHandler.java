package messageHandlers;

import DTO.LiveEventDTO;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.ConnectionFactory;
import config.Config;
import database.DatabaseHandler;
import events.RandomGeneratedEvent;
import events.ReservationEvent;

import java.io.IOException;
import java.net.ConnectException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.TimeoutException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class LiveEventsHandler implements Runnable {
    private final static String EXCHANGE = "live-events";
    private final static String ROUTING_KEY = "live-events-for-gateway";
    private final DatabaseHandler databaseHandler;
    private Channel channel;

    public LiveEventsHandler(DatabaseHandler databaseHandler) {
        this.databaseHandler = databaseHandler;
    }

    @Override
    public void run() {
        ConnectionFactory factory = new ConnectionFactory();
        Config.setConfigFactory(factory);
        try (com.rabbitmq.client.Connection connection = factory.newConnection();
             Channel channel = connection.createChannel()) {

            this.channel = channel;

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

    private String extractTransportType(String input) {
        Pattern pattern = Pattern.compile("-(TRAIN|PLANE)-");
        Matcher matcher = pattern.matcher(input);

        if (matcher.find()) {
            String extracted = matcher.group(1);
            return extracted.toLowerCase();
        }

        return null;
    }

    public void sendReservationEventMessage(ReservationEvent reservationEvent) {
        String trip_offer_id = reservationEvent.getTrip_offer_id();
        String room_type = reservationEvent.getRoom_type();
        String connection_to = reservationEvent.getConnection_id_to();

        LiveEventDTO liveEventDTO = databaseHandler.getTripById(trip_offer_id);
        liveEventDTO.setRoomType(room_type);
        liveEventDTO.setTransportType(extractTransportType(connection_to));

        ObjectMapper objectMapper = new ObjectMapper();
        try {
            objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
            String json = objectMapper.writeValueAsString(liveEventDTO);

            channel.basicPublish(EXCHANGE, ROUTING_KEY, null, json.getBytes(StandardCharsets.UTF_8));
            System.out.println("[MQ PUBLISH] Published message to LiveEvents exchange " +
                    ROUTING_KEY + " with payload: " + json);
            databaseHandler.saveLiveEventDTO(liveEventDTO);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void sendRandomGeneratedEventMessage(RandomGeneratedEvent randomGeneratedEvent) {
        ObjectMapper objectMapper = new ObjectMapper();
        try {
            objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
            String json = objectMapper.writeValueAsString(randomGeneratedEvent);

            channel.basicPublish(EXCHANGE, ROUTING_KEY, null, json.getBytes(StandardCharsets.UTF_8));
            System.out.println("[MQ PUBLISH] Published message to LiveEvents exchange " +
                    ROUTING_KEY + " with payload: " + json);
            // databaseHandler.saveLiveEventsDTO(randomGeneratedEvent);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
