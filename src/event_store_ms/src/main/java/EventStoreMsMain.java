import com.rabbitmq.client.ConnectionFactory;
import config.Config;
import database.DatabaseHandler;
import messageHandlers.HotelForEventhubMQHandler;
import messageHandlers.ReservationsForEventhubMQHandler;
import messageHandlers.TransportForEventhubMQHandler;

import java.sql.Connection;

public class EventStoreMsMain {

    public static void main(String[] args) throws Exception{
        DatabaseHandler databaseHandler = new DatabaseHandler(Config.setupDBConnection());
        Connection conn = Config.setupDBConnection();

        HotelForEventhubMQHandler hotelMQ = new HotelForEventhubMQHandler(databaseHandler);
        TransportForEventhubMQHandler transportMQ = new TransportForEventhubMQHandler(databaseHandler);
        ReservationsForEventhubMQHandler reservationMQ = new ReservationsForEventhubMQHandler(databaseHandler, hotelMQ, transportMQ);

        hotelMQ.setReservationsForEventhubMQHandler(reservationMQ);
        transportMQ.setReservationsForEventhubMQHandler(reservationMQ);

        Thread threadReservations = new Thread(reservationMQ);
        Thread threadHotel = new Thread(hotelMQ);
        Thread threadTransport = new Thread(transportMQ);
        
        threadReservations.start();
        threadHotel.start();
        threadTransport.start();
    }
}