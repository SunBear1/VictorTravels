package messageHandlers;

import DTO.HotelDTO;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.rabbitmq.client.*;
import config.Config;
import database.DatabaseHandler;
import events.HotelEvent;
import events.ReservationEvent;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class HotelForEventhubMQHandler implements Runnable{
    private final static String EXCHANGE = "hotel-events";
    private final static String ROUTING_KEY = "hotel-events-for-hotel-ms";
    private final static String QUEUE_NAME_TO_CONSUME = "hotel-events-for-eventhub-ms";
    private DatabaseHandler databaseHandler;
    private ReservationsForEventhubMQHandler reservationsMQ;
    private Channel channel;

    public HotelForEventhubMQHandler(DatabaseHandler databaseHandler) {
        this.databaseHandler = databaseHandler;
    }

    public void setReservationsForEventhubMQHandler(ReservationsForEventhubMQHandler reservationsMQ) {
        this.reservationsMQ = reservationsMQ;
    }

    @Override
    public void run() {
        System.out.println("Hello from hotel thread!");

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
        System.out.println("Message to produce in " + ROUTING_KEY + " by hotel from reservations...");

        String title = "trip_offer_hotel_room_update";
        String trip_offer_id = reservationEvent.getTrip_offer_id();
        String operation_type = (reservationEvent.getReservation_status().equals("created") ? "add" : "delete");
        String hotel_id = reservationEvent.getHotel_id();
        String room_type = reservationEvent.getRoom_type();
        HotelDTO hotelDTO = new HotelDTO(title, trip_offer_id, operation_type, hotel_id, room_type);
        databaseHandler.saveHotelDTO(hotelDTO);
        ObjectMapper objectMapper = new ObjectMapper();
        try {
            String json = objectMapper.writeValueAsString(hotelDTO);
            channel.basicPublish(EXCHANGE, ROUTING_KEY, null, json.getBytes());
            System.out.println("Message " + json + " to " + ROUTING_KEY + " published!");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void processMessage(String json) {
        try {
            System.out.println("Message from " + QUEUE_NAME_TO_CONSUME + " to consume by hotel...");
            ObjectMapper mapper = new ObjectMapper();
            HotelEvent hotelEvent = mapper.readValue(json, HotelEvent.class);
            databaseHandler.saveHotelEvent(hotelEvent);

            reservationsMQ.sendMessageFromHotel(hotelEvent);
        }
        catch (JsonProcessingException e) {
            e.printStackTrace();
        }
    }
}
