package config;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.ConnectionFactory;

import java.io.IOException;
import java.net.ConnectException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.concurrent.TimeoutException;

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
            System.out.println("Connecting to PostgresSQL...");
            Connection conn;
            Class.forName("org.postgresql.Driver");

            String dbAddress = getEnvironmentVariable("POSTGRES_ADDRESS", "localhost");
            String dbUser = getEnvironmentVariable("POSTGRES_USER", "postgres");
            String dbPassword = getEnvironmentVariable("POSTGRES_PASSWORD", "student");
            String dbName = getEnvironmentVariable("PG_DB_EVENTHUB_NAME", "rsww_17998_events");
            String dbPort = getEnvironmentVariable("POSTGRES_PORT", "5432");

            conn = DriverManager.getConnection("jdbc:postgresql://" + dbAddress + ":" + dbPort + "/" + dbName, dbUser,
                    dbPassword);
            System.out.println("Connection to PostgresSQL established.");
            return conn;
        } catch (ClassNotFoundException | SQLException e) {
            System.err.println("Connection refused to PostgresSQL. Retrying...");
            return null;
        }
    }

    public static boolean checkRabbitMQConnection() {
        ConnectionFactory factory = new ConnectionFactory();
        Config.setConfigFactory(factory);

        try {
            System.out.println("Connecting to RabbitMQ...");
            com.rabbitmq.client.Connection connection = factory.newConnection();
            Channel channel = connection.createChannel();
            if (channel != null) {
                System.out.println("Connection to RabbitMQ established.");
                return true;
            }
            System.err.println("Couldn't create channel when connecting to RabbitMQ. Retrying...");
            return false;
        } catch (ConnectException e) {
            System.err.println("Connection refused to RabbitMQ. Retrying...");
            return false;
        } catch (TimeoutException e) {
            System.err.println("Connection timeout occurred when connecting to RabbitMQ. Retrying...");
            return false;
        } catch (IOException e) {
            System.err.println("Error: I/O exception occurred.");
            e.printStackTrace();
            return false;
        }
    }

    public static String getEnvironmentVariable(String environmentVariableName, String defaultValue) {
        if (System.getenv().containsKey(environmentVariableName)) {
            return System.getenv(environmentVariableName);
        }
        return defaultValue;
    }
}
