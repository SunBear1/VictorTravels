import com.rabbitmq.client.Channel;
import com.rabbitmq.client.ConnectionFactory;

import java.io.IOException;

public class Config {
    public static void setConfigFactory(ConnectionFactory factory) {
        factory.setHost("localhost");
        factory.setVirtualHost("/victor_travels");
        factory.setUsername("admin");
        factory.setPassword("admin");
    }

    public static void setConfigQueue(Channel channel, String queueName) throws IOException {
        channel.queueDeclare(queueName, true, false, false, null);
        channel.basicQos(1);
    }
}
