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
        hotelMQ.setup();
        TransportForEventhubMQHandler transportMQ = new TransportForEventhubMQHandler(databaseHandler);
        transportMQ.setup();
        ReservationsForEventhubMQHandler reservationMQ = new ReservationsForEventhubMQHandler(databaseHandler, hotelMQ, transportMQ);
        Thread threadReservations = new Thread(reservationMQ);
        
        threadReservations.start();
    }
}