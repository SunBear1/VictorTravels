import config.Config;
import database.DatabaseHandler;
import messageHandlers.*;

import java.sql.Connection;
import java.util.concurrent.TimeUnit;

public class EventHubMsMain {

    public static void main(String[] args) throws Exception {
        DatabaseHandler databaseHandler;
        while (true) {
            Connection conn = Config.setupDBConnection();
            if (conn != null) {
                databaseHandler = new DatabaseHandler(conn);
                break;
            }
            TimeUnit.SECONDS.sleep(5);
        }
        while (!Config.checkRabbitMQConnection()) {
            TimeUnit.SECONDS.sleep(5);
        }

        HotelsHandler hotelMQ = new HotelsHandler(databaseHandler);
        TransportsHandler transportMQ = new TransportsHandler(databaseHandler);

        LiveEventsHandler liveEventsMQ = new LiveEventsHandler(databaseHandler);
        GeneratedEventsHandler generatedEventsMQ = new GeneratedEventsHandler(databaseHandler, hotelMQ, transportMQ,
                liveEventsMQ);

        ReservationsHandler reservationMQ = new ReservationsHandler(databaseHandler, hotelMQ,
                transportMQ, liveEventsMQ);

        hotelMQ.setReservationsForEventhubMQHandler(reservationMQ);
        transportMQ.setReservationsForEventhubMQHandler(reservationMQ);

        Thread threadReservations = new Thread(reservationMQ);
        Thread threadHotel = new Thread(hotelMQ);
        Thread threadTransport = new Thread(transportMQ);
        Thread threadLiveEvents = new Thread(liveEventsMQ);
        Thread threadRandomGeneratedEvents = new Thread(generatedEventsMQ);

        threadReservations.start();
        threadHotel.start();
        threadTransport.start();
        threadLiveEvents.start();
        threadRandomGeneratedEvents.start();
    }
}
