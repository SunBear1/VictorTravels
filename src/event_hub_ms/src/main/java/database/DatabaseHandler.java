package database;

import DTO.HotelEventDTO;
import DTO.LiveReservationEventsDTO;
import DTO.ReservationDTO;
import DTO.TransportEventDTO;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import events.HotelEvent;
import events.ReservationEvent;
import events.TransportEvent;

import java.sql.*;

public class DatabaseHandler {

    private final Connection conn;

    public DatabaseHandler(Connection conn) {
        this.conn = conn;
    }

    public void saveReservationEvent(ReservationEvent reservationEvent) {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
            String json = objectMapper.writeValueAsString(reservationEvent);

            String type = reservationEvent.getTitle();
            String operation = reservationEvent.getReservation_status().equals("created") ? "delete" : "add";
            String from = "ReservationMS";
            String to = "EventhubMS";
            Timestamp receiveDate = new Timestamp(System.currentTimeMillis());

            String sql = "INSERT INTO eventslog (Type, Operation, \"From\", \"To\", ReceiveDate, Body) VALUES (?, ?, ?, ?, ?, ?::json)";
            PreparedStatement stmt = conn.prepareStatement(sql);
            stmt.setString(1, type);
            stmt.setString(2, operation);
            stmt.setString(3, from);
            stmt.setString(4, to);
            stmt.setTimestamp(5, receiveDate);
            stmt.setString(6, json);

            int rowsAffected = stmt.executeUpdate();
            System.out.println("[DATABASE] " + stmt);
            System.out.println("[DATABASE] " + rowsAffected + " rows inserted");

            stmt.close();

        } catch (JsonProcessingException | SQLException e) {
            e.printStackTrace();
        }

    }

    public void saveHotelEvent(HotelEvent hotelEvent) {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
            String json = objectMapper.writeValueAsString(hotelEvent);

            String type = hotelEvent.getTitle();
            String operation = (hotelEvent.getIs_hotel_booked_up() ? "delete" : "add");
            String from = "HotelMS";
            String to = "EventhubMS";
            Timestamp receiveDate = new Timestamp(System.currentTimeMillis());

            String sql = "INSERT INTO eventslog (Type, Operation, \"From\", \"To\", ReceiveDate, Body) VALUES (?, ?, ?, ?, ?, ?::json)";
            PreparedStatement stmt = conn.prepareStatement(sql);
            stmt.setString(1, type);
            stmt.setString(2, operation);
            stmt.setString(3, from);
            stmt.setString(4, to);
            stmt.setTimestamp(5, receiveDate);
            stmt.setString(6, json);

            int rowsAffected = stmt.executeUpdate();
            System.out.println("[DATABASE] " + stmt);
            System.out.println("[DATABASE] " + rowsAffected + " rows inserted");
            stmt.close();

        } catch (JsonProcessingException | SQLException e) {
            e.printStackTrace();
        }

    }

    public void saveTransportEvent(TransportEvent transportEvent) {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
            String json = objectMapper.writeValueAsString(transportEvent);

            String type = transportEvent.getTitle();
            String operation = (transportEvent.getIs_transport_booked_up() ? "delete" : "add");
            String from = "TransportMS";
            String to = "EventhubMS";
            Timestamp receiveDate = new Timestamp(System.currentTimeMillis());

            String sql = "INSERT INTO eventslog (Type, Operation, \"From\", \"To\", ReceiveDate, Body) VALUES (?, ?, ?, ?, ?, ?::json)";
            PreparedStatement stmt = conn.prepareStatement(sql);
            stmt.setString(1, type);
            stmt.setString(2, operation);
            stmt.setString(3, from);
            stmt.setString(4, to);
            stmt.setTimestamp(5, receiveDate);
            stmt.setString(6, json);

            int rowsAffected = stmt.executeUpdate();
            System.out.println("[DATABASE] " + stmt);
            System.out.println("[DATABASE] " + rowsAffected + " rows inserted");
            stmt.close();

        } catch (JsonProcessingException | SQLException e) {
            e.printStackTrace();
        }

    }

    public void saveHotelDTO(HotelEventDTO hotelDTO) {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
            String json = objectMapper.writeValueAsString(hotelDTO);

            String type = hotelDTO.getTitle();
            String operation = hotelDTO.getOperation_type();
            String from = "EventhubMS";
            String to = "HotelMS";
            Timestamp receiveDate = new Timestamp(System.currentTimeMillis());

            String sql = "INSERT INTO eventslog (Type, Operation, \"From\", \"To\", ReceiveDate, Body) VALUES (?, ?, ?, ?, ?, ?::json)";
            PreparedStatement stmt = conn.prepareStatement(sql);
            stmt.setString(1, type);
            stmt.setString(2, operation);
            stmt.setString(3, from);
            stmt.setString(4, to);
            stmt.setTimestamp(5, receiveDate);
            stmt.setString(6, json);

            int rowsAffected = stmt.executeUpdate();
            System.out.println("[DATABASE] " + stmt);
            System.out.println("[DATABASE] " + rowsAffected + " rows inserted");
            stmt.close();
        } catch (JsonProcessingException | SQLException e) {
            e.printStackTrace();
        }
    }

    public void saveTransportDTO(TransportEventDTO transportEventDTO) {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
            String json = objectMapper.writeValueAsString(transportEventDTO);

            String type = transportEventDTO.getTitle();
            String operation = transportEventDTO.getOperation_type();
            String from = "EventhubMS";
            String to = "TransportMS";
            Timestamp receiveDate = new Timestamp(System.currentTimeMillis());

            String sql = "INSERT INTO eventslog (Type, Operation, \"From\", \"To\", ReceiveDate, Body) VALUES (?, ?, ?, ?, ?, ?::json)";
            PreparedStatement stmt = conn.prepareStatement(sql);
            stmt.setString(1, type);
            stmt.setString(2, operation);
            stmt.setString(3, from);
            stmt.setString(4, to);
            stmt.setTimestamp(5, receiveDate);
            stmt.setString(6, json);

            int rowsAffected = stmt.executeUpdate();
            System.out.println("[DATABASE] " + stmt);
            System.out.println("[DATABASE] " + rowsAffected + " rows inserted");
            stmt.close();

        } catch (JsonProcessingException | SQLException e) {
            e.printStackTrace();
        }
    }

    public void saveReservationDTO(ReservationDTO reservationDTO) {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
            String json = objectMapper.writeValueAsString(reservationDTO);

            String type = reservationDTO.getTitle();
            String operation = reservationDTO.getOperation_type();
            String from = "EventhubMS";
            String to = "ReservationMS";
            Timestamp receiveDate = new Timestamp(System.currentTimeMillis());

            String sql = "INSERT INTO eventslog (Type, Operation, \"From\", \"To\", ReceiveDate, Body) VALUES (?, ?, ?, ?, ?, ?::json)";
            PreparedStatement stmt = conn.prepareStatement(sql);
            stmt.setString(1, type);
            stmt.setString(2, operation);
            stmt.setString(3, from);
            stmt.setString(4, to);
            stmt.setTimestamp(5, receiveDate);
            stmt.setString(6, json);

            int rowsAffected = stmt.executeUpdate();
            System.out.println("[DATABASE] " + stmt);
            System.out.println("[DATABASE] " + rowsAffected + " rows inserted");
            stmt.close();

        } catch (JsonProcessingException | SQLException e) {
            e.printStackTrace();
        }
    }

    public ReservationEvent getReservationById(String id) {
        PreparedStatement stmt;
        ResultSet rs;
        try {
            String sql = "SELECT * FROM eventslog WHERE \"From\" = ? AND body->>'reservation_id' = ? ";
            stmt = conn.prepareStatement(sql);
            stmt.setString(1, "ReservationMS");
            stmt.setString(2, id);

            rs = stmt.executeQuery();
            if (rs.next()) {
                System.out.println("[DATABASE] " + stmt);
                System.out.println("[DATABASE] id: " + rs.getInt("id") + ", type: " + rs.getString("type") + ", " +
                        "operation: " + rs.getString("operation") + ", From: " + rs.getString("From") + ", " +
                        "To: " + rs.getString("To") + ", receivedate: " + rs.getTimestamp("receivedate") + "," +
                        "body: " + rs.getString("body"));

                ObjectMapper objectMapper = new ObjectMapper();

                return objectMapper.readValue(rs.getString("body"),
                        ReservationEvent.class);
            }

        } catch (SQLException | JsonProcessingException throwables) {
            throwables.printStackTrace();
        }
        return null;
    }

    public LiveReservationEventsDTO getTripById(String id) {
        PreparedStatement stmt = null;
        ResultSet rs = null;
        try {
            String sql = "SELECT * FROM tripsforliveevents WHERE offerid = " + id + ";";
            stmt = conn.prepareStatement(sql);

            rs = stmt.executeQuery();
            if (rs.next()) {
                Integer tripID = rs.getInt("tripid");
                String hotelName = rs.getString("hotelname");
                String country = rs.getString("country");
                String region = rs.getString("region");

                System.out.println("[DATABASE] " + stmt);
                System.out.println("[DATABASE] trip_id: " + tripID + ", hotel_name: " + hotelName + ", " +
                        "country: " + country + ", region: " + region);

                return new LiveReservationEventsDTO(tripID, country, region, hotelName, null, null);
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null;
    }

    public void saveLiveEventsDTO(LiveReservationEventsDTO liveEventDTO) {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
            String json = objectMapper.writeValueAsString(liveEventDTO);

            String type = liveEventDTO.getTitle();
            String operation = "forward";
            String from = "EventhubMS";
            String to = "Gateway";
            Timestamp receiveDate = new Timestamp(System.currentTimeMillis());

            String sql = "INSERT INTO eventslog (Type, Operation, \"From\", \"To\", ReceiveDate, Body) VALUES (?, ?, ?, ?, ?, ?::json)";
            PreparedStatement stmt = conn.prepareStatement(sql);
            stmt.setString(1, type);
            stmt.setString(2, operation);
            stmt.setString(3, from);
            stmt.setString(4, to);
            stmt.setTimestamp(5, receiveDate);
            stmt.setString(6, json);

            int rowsAffected = stmt.executeUpdate();
            System.out.println("[DATABASE] " + stmt);
            System.out.println("[DATABASE] " + rowsAffected + " rows inserted");
            stmt.close();

        } catch (JsonProcessingException | SQLException e) {
            e.printStackTrace();
        }
    }

    public String getTripOfferIDbyHotelID(String hotelID){
        PreparedStatement stmt = null;
        ResultSet rs = null;
        try {
            String sql = "SELECT * FROM tripsforliveevents WHERE hotelid = '" + hotelID + "';";
            stmt = conn.prepareStatement(sql);

            rs = stmt.executeQuery();
            if (rs.next()) {
                String offerID = rs.getString("offerID");

                System.out.println("[DATABASE] " + stmt);
                System.out.println("[DATABASE] offerID: " + offerID );
                return offerID;
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null;
    }

}
