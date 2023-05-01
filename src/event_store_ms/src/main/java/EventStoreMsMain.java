import com.rabbitmq.client.*;
import java.io.IOException;
import java.sql.*;
import java.sql.Connection;

public class EventStoreMsMain {

    public static void main(String[] args) throws Exception{
        Thread threadHotel = new Thread(new HotelForEventhubMQHandler());
        Thread threadTransport = new Thread(new TransportForEventhubMQHandler());
        Thread threadReservations = new Thread(new ReservationsForEventhubMQHandler());

        threadHotel.start();
        threadTransport.start();
        threadReservations.start();

        /*Connection conn = null;
        Statement stmt = null;
        ResultSet rs = null;

        try {
            Class.forName("org.postgresql.Driver");
            conn = DriverManager.getConnection("jdbc:postgresql://localhost:5432/events", "admin", "admin");

            stmt = conn.createStatement();
            rs = stmt.executeQuery("SELECT * FROM eventslog");

            while (rs.next()) {
                System.out.println(rs.getInt("id") + " " + rs.getString("type"));
            }
        }
        catch (SQLException | ClassNotFoundException e) {
            e.printStackTrace();
        }
        finally {
            try {
                rs.close();
                stmt.close();
                conn.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }*/
    }
}