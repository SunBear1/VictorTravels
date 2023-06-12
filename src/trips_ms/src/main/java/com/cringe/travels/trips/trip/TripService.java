package com.cringe.travels.trips.trip;

import com.cringe.travels.trips.trip.entity.Localisation;
import com.cringe.travels.trips.trip.entity.Transport;
import com.cringe.travels.trips.trip.entity.TripConfigurations;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.stream.Stream;

@Service
public class TripService {

    private final TripRepository repository;
    Logger logger = LoggerFactory.getLogger(TripService.class);
    SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");

    TripService(TripRepository repository) {
        this.repository = repository;
        // formatter.setTimeZone(TimeZone.getTimeZone("UTC"));
    }

    public Trip getbyTripId(String id) {
        return repository.findByTripID(id);
    }

    public Trip getByOfferId(String id) {
        return repository.findByOfferID(id);
    }

    public List<Trip> getFilteredTrips(Integer adults, Integer kidsTo3Yo, Integer kidsTo10Yo, Integer kidsTo18Yo,
            String dateFrom, String dateTo, List<String> departureRegion,
            List<String> arrivalRegion, List<String> transport, String order, String diet,
            Integer max_price) {
        // TODO Zwiększyć logowanie w tym servicie
        String query = "{$and:[{ 'is_booked_up' : false}";
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

        // If there is too many people or some parameters have negative values, return
        // empty list
        if (room_type.isEmpty()) {
            return new ArrayList<Trip>();
        }
        
        if (head_count > 0) {
            query = query + ",{\"hotel.rooms." + room_type + ".available\": { $gt: 0 }}";
        }
        if (arrivalRegion != null) {
            query = query + ",{$or: [";
            for (String region : arrivalRegion) {
                query = query + "{ \"localisation.country\": \"" + region + "\" }"; // TODO użyć StringBuildera
            }
            query = query + "]}";
        }
        if (departureRegion != null) {
            query = query + ",{ $or: [";
            for (String region : departureRegion) {
                query = query + "{ \"from." + region + ".plane.transportBookedUp\": false }, { \"from." + region
                        + ".train.transportBookedUp\": false }"; // TODO użyć StringBuildera
            }
            query = query + "]}";
        }
        if (transport != null && !transport.contains("own")) {
            query = query + ",{\"transport_types\": {\"$in\": [";
            for (String transport_type : transport) {
                query = query + "\"" + transport_type + "\","; // TODO użyć StringBuildera
            }
            query = query + "]}}";
        }
        if (diet != null) {
            query = query + ",{$or: [";
                query = query + "{ \"hotel.diet." + diet + "\": { $exists: true } }"; // TODO użyć StringBuildera
            query = query + "]}";
        }

        // TODO sprawdzić czy format dateFrom oraz DateTo jest poprawny

        if (dateFrom != null)
            query = query + ",{date_from: { $gte: ISODate('" + dateFrom + "') }}";
        if (dateTo != null)
            query = query + ",{date_to: { $lte: ISODate('" + dateTo + "') }}";

        query = query + "]}";
        logger.info(query);
        List<Trip> filteredTrips = repository.findTripsByCustomQuery(query);
        for (int i = 0; i < filteredTrips.size(); i++) {
            int roomPrice = filteredTrips.get(i).getHotel().getRooms().get(room_type).getCost();
            int dietPrice = filteredTrips.get(i).getHotel().getDiet().get(diet);
            float tripPrice = calculateTripPrices(adults, kidsTo3Yo, kidsTo10Yo, kidsTo18Yo, roomPrice, null, null,
                    null, dietPrice);
            filteredTrips.get(i).setPrice(tripPrice);
            if (max_price != null && tripPrice > max_price) {
                filteredTrips.remove(i);
                i--;
                break;
            }

            removeBookedUpTransport(filteredTrips.get(i).getTo());
            removeBookedUpTransport(filteredTrips.get(i).getFrom());
        }

        return filteredTrips;
    }

    public Float calculateTripPrices(Integer adults, Integer kidsTo3Yo, Integer kidsTo10Yo, Integer kidsTo18Yo,
            Integer room_cost, Integer number_of_days, Integer transport_to_cost, Integer transport_from_cost,
            Integer diet_cost) {
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
        if (room_cost == null)
            room_cost = 700;

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
        if (head_count == 1)
            return "studio";
        else if (head_count == 2)
            return "small";
        else if (head_count == 3)
            return "medium";
        else if (head_count == 4)
            return "large";
        else if (head_count < 7)
            return "apartment";
        else
            return "";
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

    private void removeBookedUpTransport(HashMap<String, Transport> transports) {
        for (Transport transport : transports.values()) {
            if (transport.getPlane() != null && transport.getPlane().isTransportBookedUp()) {
                transport.setPlane(null);
            }
            if (transport.getTrain() != null && transport.getTrain().isTransportBookedUp()) {
                transport.setTrain(null);
            }
        }
    }
}
