package database;

import DTO.HotelDTO;
import DTO.LiveEventsDTO;
import DTO.ReservationDTO;
import DTO.TransportDTO;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import events.HotelEvent;
import events.ReservationEvent;
import events.TransportEvent;

import java.sql.*;

public class DatabaseHandler {

    private Connection conn;

    public DatabaseHandler(Connection conn) {
        this.conn = conn;
    }

    public boolean saveReservationEvent(ReservationEvent reservationEvent) {
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
            System.out.println("[DATABASE] " + stmt.toString());
            System.out.println("[DATABASE] " + rowsAffected + " rows inserted");

            stmt.close();

            return true;
        } catch (JsonProcessingException | SQLException e) {
            e.printStackTrace();
            return false;
        }

    }

    public boolean saveHotelEvent(HotelEvent hotelEvent) {
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
            System.out.println("[DATABASE] " + stmt.toString());
            System.out.println("[DATABASE] " + rowsAffected + " rows inserted");
            stmt.close();

            return true;
        } catch (JsonProcessingException | SQLException e) {
            e.printStackTrace();
            return false;
        }

    }

    public boolean saveTransportEvent(TransportEvent transportEvent) {
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
            System.out.println("[DATABASE] " + stmt.toString());
            System.out.println("[DATABASE] " + rowsAffected + " rows inserted");
            stmt.close();

            return true;
        } catch (JsonProcessingException | SQLException e) {
            e.printStackTrace();
            return false;
        }

    }

    public boolean saveHotelDTO(HotelDTO hotelDTO) {
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
            System.out.println("[DATABASE] " + stmt.toString());
            System.out.println("[DATABASE] " + rowsAffected + " rows inserted");
            stmt.close();

            return true;
        } catch (JsonProcessingException | SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean saveTransportDTO(TransportDTO transportDTO) {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
            String json = objectMapper.writeValueAsString(transportDTO);

            String type = transportDTO.getTitle();
            String operation = transportDTO.getOperation_type();
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
            System.out.println("[DATABASE] " + stmt.toString());
            System.out.println("[DATABASE] " + rowsAffected + " rows inserted");
            stmt.close();

            return true;
        } catch (JsonProcessingException | SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean saveReservationDTO(ReservationDTO reservationDTO) {
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
            System.out.println("[DATABASE] " + stmt.toString());
            System.out.println("[DATABASE] " + rowsAffected + " rows inserted");
            stmt.close();

            return true;
        } catch (JsonProcessingException | SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public ReservationEvent getReservationById(String id) {
        PreparedStatement stmt = null;
        ResultSet rs = null;
        try {
            String sql = "SELECT * FROM eventslog WHERE \"From\" = ? AND body->>'reservation_id' = ? ";
            stmt = conn.prepareStatement(sql);
            stmt.setString(1, "ReservationMS");
            stmt.setString(2, id);

            rs = stmt.executeQuery();
            if (rs.next()) {
                System.out.println(rs.getInt("id"));
                System.out.println(rs.getString("type"));
                System.out.println(rs.getString("operation"));
                System.out.println(rs.getString("From"));
                System.out.println(rs.getString("To"));
                System.out.println(rs.getTimestamp("receivedate"));
                System.out.println(rs.getString("body"));

                System.out.println("[DATABASE] " + stmt.toString());
                System.out.println("[DATABASE] 1 row selected");
                System.out.println("[DATABASE] id: " + rs.getInt("id") + ", type: " + rs.getString("type") + ", " +
                        "operation: " + rs.getString("operation") + ", From: " + rs.getString("From") + ", " +
                        "To: " + rs.getString("To") + ", receivedate: " + rs.getTimestamp("receivedate") + "," +
                        "body: " + rs.getString("body"));

                ObjectMapper objectMapper = new ObjectMapper();
                ReservationEvent reservationEventTmp = objectMapper.readValue(rs.getString("body"),
                        ReservationEvent.class);
                return reservationEventTmp;
            }

        } catch (SQLException | JsonProcessingException throwables) {
            throwables.printStackTrace();
        }
        return null;
    }

    public LiveEventsDTO getTripbyId(String id) {
        PreparedStatement stmt = null;
        ResultSet rs = null;
        try {
            String sql = "SELECT * FROM tripsforliveevents WHERE offerid = " + id + ";";
            stmt = conn.prepareStatement(sql);
            // stmt.setString(1, id);

            rs = stmt.executeQuery();
            if (rs.next()) {
                Integer tripID = rs.getInt("tripid");
                String hotelName = rs.getString("hotelname");
                String country = rs.getString("country");
                String region = rs.getString("region");

                System.out.println("[DATABASE] " + stmt.toString());
                System.out.println("[DATABASE] 1 row selected");
                System.out.println("[DATABASE] trip_id: " + tripID + ", hotel_name: " + hotelName + ", " +
                        "country: " + country + ", region: " + region);

                return new LiveEventsDTO(tripID, country, region, hotelName, null, null);
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null;
    }

    public boolean saveLiveEventsDTO(LiveEventsDTO liveeventDTO) {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
            String json = objectMapper.writeValueAsString(liveeventDTO);

            String type = liveeventDTO.getTitle();
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
            System.out.println("[DATABASE] " + stmt.toString());
            System.out.println("[DATABASE] " + rowsAffected + " rows inserted");
            stmt.close();

            return true;
        } catch (JsonProcessingException | SQLException e) {
            e.printStackTrace();
            return false;
        }
    }
}
