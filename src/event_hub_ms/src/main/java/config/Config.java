package config;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.ConnectionFactory;
import java.sql.Connection;
import java.io.IOException;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Map;

public class Config {

    public static void setConfigFactory(ConnectionFactory factory) {
        String factoryHost = getEnvironmentVariable("RABBITMQ_ADDRESS", "localhost");
        String factoryPort = getEnvironmentVariable("RABBITMQ_PORT", "17998");
        factory.setHost(factoryHost);
        factory.setVirtualHost("/victor_travels");
        factory.setUsername("admin");
        factory.setPassword("admin");
        factory.setPort(Integer.parseInt(factoryPort));
    }

    public static void setConfigQueue(Channel channel, String queueName) throws IOException {
        channel.basicQos(1);
    }

    public static Connection setupDBConnection() {
        try {
            Connection conn;
            Class.forName("org.postgresql.Driver");

            String dbAddress = getEnvironmentVariable("POSTGRES_ADDRESS", "localhost");
            String dbUser = getEnvironmentVariable("POSTGRES_USER", "postgres");
            String dbPassword = getEnvironmentVariable("POSTGRES_PASSWORD", "student");
            String dbName = getEnvironmentVariable("PG_DB_EVENTHUB_NAME", "rsww_17998_events");
            String dbPort = getEnvironmentVariable("POSTGRES_PORT", "5432");

            conn = DriverManager.getConnection("jdbc:postgresql://" + dbAddress + ":" + dbPort + "/" + dbName, dbUser,
                    dbPassword);
            return conn;
        } catch (ClassNotFoundException | SQLException e) {
            e.printStackTrace();
        }
        return null;
    }

    public static String getEnvironmentVariable(String environmentVariableName, String defaultValue) {
        if (System.getenv().containsKey(environmentVariableName)) {
            return System.getenv(environmentVariableName);
        }
        return defaultValue;
    }
}
