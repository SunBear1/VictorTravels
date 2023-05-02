package config;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.ConnectionFactory;
import java.sql.Connection;
import java.io.IOException;
import java.sql.DriverManager;
import java.sql.SQLException;

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

    public static Connection setupDBConnection() {
        try {
            Connection conn;
            Class.forName("org.postgresql.Driver");
            conn = DriverManager.getConnection("jdbc:postgresql://localhost:5432/events", "admin", "admin");
            return conn;
        }
        catch (ClassNotFoundException | SQLException e) {
            e.printStackTrace();
        }
        return null;
    }
}
