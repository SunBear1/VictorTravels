package messageHandlers;

import DTO.ReservationDTO;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.rabbitmq.client.*;
import config.Config;
import database.DatabaseHandler;
import events.HotelEvent;
import events.RandomGeneratedEvent;
import events.ReservationEvent;
import events.TransportEvent;

import java.io.IOException;
import java.net.ConnectException;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.concurrent.TimeoutException;

public class GeneratedEventsHandler implements Runnable {
    private final static String EXCHANGE = "reservations";
    private final static String ROUTING_KEY = "reservations-for-reservations-ms";
    private final static String QUEUE_NAME_TO_CONSUME = "generated-random-events-for-eventhub-ms";
    private final DatabaseHandler databaseHandler;
    private Channel channel;
    private final HotelsHandler hotelMQ;
    private final TransportsHandler transportMQ;
    private final LiveEventsHandler liveEventsMQ;

    public GeneratedEventsHandler(DatabaseHandler databaseHandler, HotelsHandler hotelMQ,
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
                    System.out.println(
                            "[MQ CONSUME] Received message from EventGeneratorMS queue " + QUEUE_NAME_TO_CONSUME
                                    + " with payload: " + message);
                    consumeMessageFromEventGenerator(message);
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

    public void consumeMessageFromEventGenerator(String json) {
        try {
            ObjectMapper mapper = new ObjectMapper();
            RandomGeneratedEvent randomGeneratedEvent = mapper.readValue(json, RandomGeneratedEvent.class);
            // TODO databaseHandler.saveReservationEvent(reservationEvent);

            if (randomGeneratedEvent.getType().equals("hotel")) {
                hotelMQ.prepareGeneratedEventMessage(randomGeneratedEvent);
            }
            if (randomGeneratedEvent.getType().equals("connection")) {
                transportMQ.prepareGeneratedEventMessage(randomGeneratedEvent);
            }
            liveEventsMQ.sendRandomGeneratedEventMessage(randomGeneratedEvent);

        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }
    }
}
