package messageHandlers;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.rabbitmq.client.*;
import config.Config;
import database.DatabaseHandler;
import events.ReservationEvent;
import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class ReservationsForEventhubMQHandler implements Runnable{
    private final static String QUEUE_NAME = "reservations-for-eventhub-ms";
    private final DatabaseHandler databaseHandler;
    private final HotelForEventhubMQHandler hotelMQ;
    private final TransportForEventhubMQHandler transportMQ;

    public ReservationsForEventhubMQHandler(DatabaseHandler databaseHandler, HotelForEventhubMQHandler hotelMQ, TransportForEventhubMQHandler  transportMQ) {
        this.databaseHandler = databaseHandler;
        this.transportMQ = transportMQ;
        this.hotelMQ = hotelMQ;
    }

    @Override
    public void run() {
        System.out.println("Hello from thread " + QUEUE_NAME);

        ConnectionFactory factory = new ConnectionFactory();
        Config.setConfigFactory(factory);
        try (com.rabbitmq.client.Connection connection = factory.newConnection();
             Channel channel = connection.createChannel()) {

            DefaultConsumer consumer = new DefaultConsumer(channel) {
                @Override
                public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {
                    String message = new String(body, "UTF-8");
                    System.out.println(" [x] Received '" + message + "'" + " from " + QUEUE_NAME);
                    processMessage(message);
                    channel.basicAck(envelope.getDeliveryTag(), false);
                }
            };

            channel.basicConsume(QUEUE_NAME, false, consumer);

            while (true) {
                ;
            }

        } catch (TimeoutException | IOException e) {
            e.printStackTrace();
        }
    }

    public void processMessage(String json) {
        try {
            System.out.println("Some operations for " + QUEUE_NAME + "...");
            ObjectMapper mapper = new ObjectMapper();
            ReservationEvent reservationEvent = mapper.readValue(json, ReservationEvent.class);
            databaseHandler.saveReservationEvent(reservationEvent);

            if (!reservationEvent.getReservation_status().equals("finalize")) {
                if (!reservationEvent.getReservation_status().equals("created")) {
                    ReservationEvent tmp = databaseHandler.getReservationById(reservationEvent.getReservation_id());

                    reservationEvent.setHotel_id(tmp.getHotel_id());
                    reservationEvent.setRoom_type(tmp.getRoom_type());
                    reservationEvent.setConnection_id(tmp.getConnection_id());
                }
                hotelMQ.processMessage(reservationEvent);
                transportMQ.processMessage(reservationEvent);
            }
        }
        catch (JsonProcessingException e) {
            e.printStackTrace();
        }
    }
}
