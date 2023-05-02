package messageHandlers;

import DTO.HotelDTO;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.rabbitmq.client.*;
import config.Config;
import database.DatabaseHandler;
import events.ReservationEvent;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class HotelForEventhubMQHandler {
    private final static String QUEUE_NAME = "hotel-events-for-eventhub-ms";
    private DatabaseHandler databaseHandler;
    private Channel channel;

    public HotelForEventhubMQHandler(DatabaseHandler databaseHandler) {
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

        String title = "trip_offer_hotel_room_update";
        Integer trip_offer_id = reservationEvent.getTrip_offer_id();
        String operation_type = (reservationEvent.getReservation_status().equals("created") ? "add" : "delete");
        String hotel_id = reservationEvent.getHotel_id();
        String room_type = reservationEvent.getRoom_type();

        HotelDTO hotelDTO = new HotelDTO(title, trip_offer_id, operation_type, hotel_id, room_type);
        databaseHandler.saveHotelDTO(hotelDTO);

        ObjectMapper objectMapper = new ObjectMapper();
        try {
            String json = objectMapper.writeValueAsString(hotelDTO);
            channel.basicPublish("", QUEUE_NAME, null, json.getBytes());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
