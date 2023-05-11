package com.cringe.travels.trips.trip;

import com.cringe.travels.trips.trip.entity.Localisation;
import com.cringe.travels.trips.trip.entity.TripConfigurations;
import org.json.JSONArray;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.stream.Stream;

@Service
public class TripService {

    private final TripRepository repository;
    Logger logger = LoggerFactory.getLogger(TripService.class);
    SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");


    TripService(TripRepository repository) {
        this.repository = repository;
        //formatter.setTimeZone(TimeZone.getTimeZone("UTC"));
    }

    public List<Trip> getAll() {
        return repository.findAll();
    }

    public List<Trip> getAllActive() {
        return repository.findAllActiveTrips();
    }

    public void updateHotelsRooms(JSONObject jsonObject) {

        JSONArray listIds = jsonObject.getJSONArray("trip_offers_id");
        String operationType = jsonObject.getString("operation_type");
        String roomType = jsonObject.getString("room_type");

        for (int i = 0; i < listIds.length(); i++) {
            String id = listIds.getString(i);
            Optional<Trip> tripOpt = repository.findById(id);
            if (tripOpt.isPresent()) {
                Trip trip = tripOpt.get();
                int freeSeats = trip.getHotel().getRooms().get(roomType).getAvailable();
                logger.info("BEFORE: TRIP: " + trip.getId() + "\n Room type:" + roomType + "\n seats left:" + freeSeats);
                if (operationType.equals("add")) {
                    freeSeats++;
                } else {
                    freeSeats--;
                }
                trip.getHotel().getRooms().get(roomType).setAvailable(freeSeats);
                repository.save(trip);
                logger.info("NOW: TRIP: " + trip.getId() + "\n Room type:" + roomType + "\n seats left:" + freeSeats);
            } else {
                logger.info("NO TRIP IN DB WITH ID:" + id);
            }
        }
    }

    public void updateTripStatus(JSONObject jsonObject) {

        JSONArray listIds = jsonObject.getJSONArray("trip_offers_id");
        boolean isHotelBookedUp = jsonObject.getBoolean("is_hotel_booked_up");

        for (int i = 0; i < listIds.length(); i++) {
            String id = listIds.getString(i);
            Optional<Trip> tripOpt = repository.findById(id);
            if (tripOpt.isPresent()) {
                Trip trip = tripOpt.get();
                trip.setBookedUp(isHotelBookedUp);
                repository.save(trip);
                logger.info("UPDATED TRIP STATUS IN TRIP: " + trip.getId() + "\n bookedUp:" + isHotelBookedUp);

            } else {
                logger.info("NO TRIP IN DB WITH ID:" + id);
            }
        }
    }

    public void updateTransport(JSONObject jsonObject) {

        JSONArray listIds = jsonObject.getJSONArray("trip_offers_id");
        String connectionIdTO = jsonObject.getString("connection_id_to");
        String connectionIdFrom = jsonObject.getString("connection_id_from");
        String operationType = jsonObject.getString("operation_type");
        int headCount = jsonObject.getInt("head_count");


        for (int i = 0; i < listIds.length(); i++) {
            String id = listIds.getString(i);
            Optional<Trip> tripOpt = repository.findById(id);
            if (tripOpt.isPresent()) {
                Trip trip = tripOpt.get();
                trip.getFrom().forEach((key, transport) -> {
                    if (transport.getPlane() != null) {
                        if (transport.getPlane().getId().equals(connectionIdFrom)) {
                            int seatsLeft = transport.getPlane().getSeatsLeft();
                            logger.info("BEFORE: TRIP: " + trip.getId() + "\n Connection ID:" + connectionIdFrom + "\n seats left:" + seatsLeft);
                            if (operationType.equals("add")) {
                                seatsLeft = seatsLeft + headCount;
                            } else {
                                seatsLeft = seatsLeft - headCount;
                            }
                            transport.getPlane().setSeatsLeft(seatsLeft);
                            repository.save(trip);
                            logger.info("NOW: TRIP: " + trip.getId() + "\n Connection ID:" + connectionIdFrom + "\n seats left:" + seatsLeft);
                        }
                    }

                    if (transport.getTrain() != null) {
                        if (transport.getTrain().getId().equals(connectionIdFrom)) {
                            int seatsLeft = transport.getTrain().getSeatsLeft();
                            logger.info("BEFORE: TRIP: " + trip.getId() + "\n Connection ID:" + connectionIdFrom + "\n seats left:" + seatsLeft);
                            if (operationType.equals("add")) {
                                seatsLeft = seatsLeft + headCount;
                            } else {
                                seatsLeft = seatsLeft - headCount;
                            }
                            transport.getTrain().setSeatsLeft(seatsLeft);
                            repository.save(trip);
                            logger.info("NOW: TRIP: " + trip.getId() + "\n Connection ID:" + connectionIdFrom + "\n seats left:" + seatsLeft);
                        }
                    }
                });


                trip.getTo().forEach((key, transport) -> {
                    if (transport.getPlane() != null) {
                        if (transport.getPlane().getId().equals(connectionIdTO)) {
                            int seatsLeft = transport.getPlane().getSeatsLeft();
                            logger.info("BEFORE: TRIP: " + trip.getId() + "\n Connection ID:" + connectionIdTO + "\n seats left:" + seatsLeft);
                            if (operationType.equals("add")) {
                                seatsLeft = seatsLeft + headCount;
                            } else {
                                seatsLeft = seatsLeft - headCount;
                            }
                            transport.getPlane().setSeatsLeft(seatsLeft);
                            repository.save(trip);
                            logger.info("NOW: TRIP: " + trip.getId() + "\n Connection ID:" + connectionIdTO + "\n seats left:" + seatsLeft);
                        }
                    }

                    if (transport.getTrain() != null) {
                        if (transport.getTrain().getId().equals(connectionIdTO)) {
                            int seatsLeft = transport.getTrain().getSeatsLeft();
                            logger.info("BEFORE: TRIP: " + trip.getId() + "\n Connection ID:" + connectionIdTO + "\n seats left:" + seatsLeft);
                            if (operationType.equals("add")) {
                                seatsLeft = seatsLeft + headCount;
                            } else {
                                seatsLeft = seatsLeft - headCount;
                            }
                            transport.getTrain().setSeatsLeft(seatsLeft);
                            repository.save(trip);
                            logger.info("NOW: TRIP: " + trip.getId() + "\n Connection ID:" + connectionIdTO + "\n seats left:" + seatsLeft);
                        }
                    }
                });
            } else {
                logger.info("NO TRIP IN DB WITH ID:" + id);
            }
        }
    }

    public void updateTransportStatus(JSONObject jsonObject) {

        JSONArray listIds = jsonObject.getJSONArray("trip_offers_id");
        String connectionId = jsonObject.getString("connection_id");
        boolean transportBookedUp = jsonObject.getBoolean("is_transport_booked_up");


        for (int i = 0; i < listIds.length(); i++) {
            String id = listIds.getString(i);
            Optional<Trip> tripOpt = repository.findById(id);
            if (tripOpt.isPresent()) {
                Trip trip = tripOpt.get();
                trip.getFrom().forEach((key, transport) -> {
                    if (transport.getPlane() != null) {
                        if (transport.getPlane().getId().equals(connectionId)) {
                            transport.getPlane().setTransportBookedUp(transportBookedUp);
                            repository.save(trip);
                            logger.info("UPDATED TRANSPORT STATUS IN TRIP: " + trip.getId() + "\n connection id: " + connectionId + "\n bookedUp:" + transportBookedUp);
                        }
                    }

                    if (transport.getTrain() != null) {
                        if (transport.getTrain().getId().equals(connectionId)) {
                            transport.getTrain().setTransportBookedUp(transportBookedUp);
                            repository.save(trip);
                            logger.info("UPDATED TRANSPORT STATUS IN TRIP: " + trip.getId());
                        }
                    }

                });

                trip.getTo().forEach((key, transport) -> {
                    if (transport.getPlane() != null) {
                        if (transport.getPlane().getId().equals(connectionId)) {
                            transport.getPlane().setTransportBookedUp(transportBookedUp);
                            repository.save(trip);
                            logger.info("UPDATED TRANSPORT STATUS IN TRIP: " + trip.getId() + "\n connection id: " + connectionId + "\n bookedUp:" + transportBookedUp);
                        }
                    }

                    if (transport.getTrain() != null) {
                        if (transport.getTrain().getId().equals(connectionId)) {
                            transport.getTrain().setTransportBookedUp(transportBookedUp);
                            repository.save(trip);
                            logger.info("UPDATED TRANSPORT STATUS IN TRIP: " + trip.getId());
                        }
                    }

                });
            } else {
                logger.info("NO TRIP IN DB WITH ID:" + id);
            }
        }
    }

    public Trip getbyTripId(String id) {
        return repository.findByTripID(id);
    }

    public Trip getByOfferId(String id) {
        return repository.findByOfferID(id);
    }

    public List<Trip> getFilteredTrips(Integer adults, Integer kidsTo3Yo, Integer kidsTo10Yo, Integer kidsTo18Yo,
                                       String dateFrom, String dateTo, List<String> departureRegion,
                                       List<String> arrivalRegion, List<String> transport, String order, List<String> diet,
                                       Integer max_price) {
        // TODO Zwiększyć logowanie w tym servicie
        String query = "{ ";
        int head_count = 0;
        if (adults != null)
            head_count += adults;
        if (kidsTo3Yo != null)
            head_count += kidsTo3Yo;
        if (kidsTo10Yo != null)
            head_count += kidsTo10Yo;
        if (kidsTo18Yo != null)
            head_count += kidsTo18Yo;

        String room_type = getRoomTypeForPeople(head_count);
        if (head_count > 0) {
            query = query + "\"hotel.rooms." + room_type + ".available\": { $gt: 0 }";
        }
        if (arrivalRegion != null) {
            query = query + "$or: [";
            for (String region : arrivalRegion) {
                query = query + "{ \"localisation.country\": \"" + region + "\" }"; // TODO użyć StringBuildera
            }
            query = query + "]";
        }
        if (departureRegion != null) {
            query = query + "$and: [ { $or: [";
            for (String region : departureRegion) {
                query = query + "{ \"from." + region + ".plane.transportBookedUp\": false }, { \"from." + region + ".train.transportBookedUp\": false }"; // TODO użyć StringBuildera
            }
            query = query + "]}]";
        }
        if (transport != null) {
            query = query + "\"transport_types\": {\"$in\": [";
            for (String transport_type : transport) { // TODO nie ma sprawdzania własnego transportu, czy to działa? Trzeba przetestować
                query = query + "\"" + transport_type + "\","; // TODO użyć StringBuildera
            }
            query = query + "]}";
        }
        if (diet != null) {
            query = query + "$or: [";
            for (String diet_option : diet) {
                query = query + "{ \"hotel.diet." + diet_option + "\": { $exists: true } }"; // TODO użyć StringBuildera
            }
            query = query + "]";
        }

        // TODO sprawdzić czy format dateFrom oraz DateTo jest poprawny

        if (dateFrom != null)
            query = query + ",date_from: { $gte: ISODate('" + dateFrom + "') }";
        if (dateTo != null)
            query = query + ",date_to: { $lte: ISODate('" + dateTo + "') }";

        query = query + " }";

        List<Trip> filteredTrips = repository.findTripsByCustomQuery(query);
        for (int i = 0; i < filteredTrips.size(); i++) {
            var roomPrice = filteredTrips.get(i).getHotel().getRooms().get(room_type).getCost();
            float tripPrice = calculateTripPrices(adults, kidsTo3Yo, kidsTo10Yo, kidsTo18Yo, roomPrice, null, null, null, null);
            filteredTrips.get(i).setPrice(calculateTripPrices(adults, kidsTo3Yo, kidsTo10Yo, kidsTo18Yo, roomPrice, null, null, null, null));
            if (max_price != null && tripPrice > max_price) {
                filteredTrips.remove(i);
                i--;
            }
        }

        return filteredTrips;
    }


    public Float calculateTripPrices(Integer adults, Integer kidsTo3Yo, Integer kidsTo10Yo, Integer kidsTo18Yo, Integer room_cost, Integer number_of_days, Integer transport_to_cost, Integer transport_from_cost, Integer diet_cost) {
        float totalPrice = 0;
        float provision = 1.1F;

        if (number_of_days == null)
            number_of_days = 1;
        if (transport_to_cost == null)
            transport_to_cost = 90;
        if (transport_from_cost == null)
            transport_from_cost = 90;
        if (diet_cost == null)
            diet_cost = 500;
        if (kidsTo3Yo == null)
            kidsTo3Yo = 0;
        if (adults == null)
            adults = 0;
        if (kidsTo10Yo == null)
            kidsTo10Yo = 0;
        if (kidsTo18Yo == null)
            kidsTo18Yo = 0;

        for (int i = 0; i < kidsTo3Yo; i++) {
            float transportCost = 0;
            float hotelCost = (float) ((diet_cost + room_cost) * number_of_days * 0.1);
            totalPrice = totalPrice + (transportCost + hotelCost) * provision;
        }
        for (int i = 0; i < kidsTo10Yo; i++) {
            float transportCost = (float) ((transport_to_cost + transport_from_cost) * 0.5);
            float hotelCost = (float) ((diet_cost + room_cost) * number_of_days * 0.5);
            totalPrice = totalPrice + (transportCost + hotelCost) * provision;
        }
        for (int i = 0; i < kidsTo18Yo; i++) {
            float transportCost = (float) ((transport_to_cost + transport_from_cost) * 0.6);
            float hotelCost = (float) ((diet_cost + room_cost) * number_of_days * 0.7);
            totalPrice = totalPrice + (transportCost + hotelCost) * provision;
        }
        for (int i = 0; i < adults; i++) {
            float transportCost = (float) (transport_to_cost + transport_from_cost);
            float hotelCost = (float) ((diet_cost + room_cost) * number_of_days);
            totalPrice = totalPrice + (transportCost + hotelCost) * provision;
        }
        return totalPrice;
    }


    public String getRoomTypeForPeople(Integer head_count) {
        if (head_count == 1) {
            return "studio";
        } else if (head_count == 2) {
            return "small";
        } else if (head_count == 3) {
            return "medium";
        } else if (head_count == 4) {
            return "large";
        } else {
            return "apartment";
        }
    }

    public List<Localisation> getArrivalLocations(List<Trip> trips) {
        List<Localisation> arrivalLocations = new ArrayList<>();
        for (Trip trip : trips) {
            Localisation locations = trip.getLocalisation();
            if (!arrivalLocations.contains(locations))
                arrivalLocations.add(locations);
        }
        return arrivalLocations;
    }

    public List<String> getTransportTypes(List<Trip> trips) {
        List<String> transportTypes = new ArrayList<>();
        for (Trip trip : trips) {
            transportTypes.addAll(trip.getTransport_types());
        }
        return transportTypes.stream().distinct().toList();
    }

    public List<String> getDepartureLocations(List<Trip> trips) {
        return trips.stream()
                .flatMap(trip -> Stream.concat(trip.getFrom().keySet().stream(), trip.getTo().keySet().stream()))
                .distinct()
                .toList();
    }

    public TripConfigurations queryForTripConfigurations() {
        List<Trip> trips = repository.findAllActiveTrips();

        List<Localisation> arrivalLocations = getArrivalLocations(trips);
        List<String> transportTypes = getTransportTypes(trips);
        List<String> departureLocations = getDepartureLocations(trips);

        return new TripConfigurations(departureLocations, arrivalLocations, transportTypes);
    }

}
