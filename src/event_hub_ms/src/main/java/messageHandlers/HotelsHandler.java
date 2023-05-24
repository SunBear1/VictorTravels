package messageHandlers;

import DTO.HotelDTO;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.rabbitmq.client.*;
import config.Config;
import database.DatabaseHandler;
import events.HotelEvent;
import events.ReservationEvent;

import java.io.IOException;
import java.net.ConnectException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.TimeoutException;

public class HotelsHandler implements Runnable {
    private final static String EXCHANGE = "hotel-events";
    private final static String ROUTING_KEY = "hotel-events-for-hotel-ms";
    private final static String QUEUE_NAME_TO_CONSUME = "hotel-events-for-eventhub-ms";
    private final DatabaseHandler databaseHandler;
    private ReservationsHandler reservationsMQ;
    private Channel channel;

    public HotelsHandler(DatabaseHandler databaseHandler) {
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
                    System.out.println("[MQ CONSUME] Received message from hotelMS queue " + QUEUE_NAME_TO_CONSUME
                            + " with payload: " + message);
                    consumeMessageFromHotel(message);
                    channel.basicAck(envelope.getDeliveryTag(), false);
                }
            };

            channel.basicConsume(QUEUE_NAME_TO_CONSUME, false, consumer);

            while (true) {
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

    public void sendMessage(ReservationEvent reservationEvent) {
        String title = "trip_offer_hotel_room_update";
        String trip_offer_id = reservationEvent.getTrip_offer_id();
        String operation_type = (reservationEvent.getReservation_status().equals("created") ? "delete" : "add");
        String hotel_id = reservationEvent.getHotel_id();
        String room_type = reservationEvent.getRoom_type();
        HotelDTO hotelDTO = new HotelDTO(title, trip_offer_id, operation_type, hotel_id, room_type);
        databaseHandler.saveHotelDTO(hotelDTO);
        ObjectMapper objectMapper = new ObjectMapper();
        try {
            objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
            String json = objectMapper.writeValueAsString(hotelDTO);
            channel.basicPublish(EXCHANGE, ROUTING_KEY, null, json.getBytes());
            System.out.println("[MQ PUBLISH] Published message to HotelMS exchange " +
                    ROUTING_KEY + " with payload: " + json);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void consumeMessageFromHotel(String json) {
        try {
            ObjectMapper mapper = new ObjectMapper();
            HotelEvent hotelEvent = mapper.readValue(json, HotelEvent.class);
            databaseHandler.saveHotelEvent(hotelEvent);

            reservationsMQ.sendMessageFromHotel(hotelEvent);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }
    }
}
