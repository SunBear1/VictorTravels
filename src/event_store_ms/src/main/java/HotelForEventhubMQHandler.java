import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.rabbitmq.client.*;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class HotelForEventhubMQHandler implements Runnable{
    private final static String QUEUE_NAME = "hotel-events-for-eventhub-ms";

    @Override
    public void run() {
        System.out.println("Hello from thread " + QUEUE_NAME);

        ConnectionFactory factory = new ConnectionFactory();
        Config.setConfigFactory(factory);
        try (Connection connection = factory.newConnection();
             Channel channel = connection.createChannel()) {

            String message = "Hello World!";
            String message1 = "Hello World111!";
            String message2 = "Hello World222!";

            //channel.basicPublish("", QUEUE_NAME, null, message.getBytes());
            //channel.basicPublish("", QUEUE_NAME, null, message1.getBytes());
            //channel.basicPublish("", QUEUE_NAME, null, message2.getBytes());
            System.out.println(" [x] Sent '" + message + "'" + " in " + QUEUE_NAME);

            DefaultConsumer consumer = new DefaultConsumer(channel) {
                @Override
                public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {
                    String message = new String(body, "UTF-8");
                    System.out.println(" [x] Received '" + message + "'" + " from " + QUEUE_NAME);
                    someFunc(message);
                    channel.basicAck(envelope.getDeliveryTag(), false);
                }
            };

            //channel.basicConsume(QUEUE_NAME, false, consumer);

            for (int i=0; i<4; i++) {
                int x = 1;
                Hotel hotel = new Hotel("val1", "val2", "val3");
                ObjectMapper mapper = new ObjectMapper();
                String json = mapper.writeValueAsString(hotel);
                channel.basicPublish("", QUEUE_NAME, null, json.getBytes());
                Thread.sleep(1000);
            }

        } catch (TimeoutException | InterruptedException | IOException e) {
            e.printStackTrace();
        }
    }

    public void someFunc(String json) {
        try {
            System.out.println("Some operations for " + QUEUE_NAME + "...");
            ObjectMapper objectMapper = new ObjectMapper();
            Hotel hotel = objectMapper.readValue(json, Hotel.class);

            System.out.println(hotel.hotel_id);
            System.out.println(hotel.room_type);
            System.out.println(hotel.connection_id);
        }
        catch (JsonProcessingException e) {
            e.printStackTrace();
        }
    }
}
