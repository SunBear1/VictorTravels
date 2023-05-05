package com.cringe.travels.trips.trip;

import java.util.List;
import java.util.Optional;

import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.stereotype.Service;

@Service
public class TripService {

    private final TripRepository repository;

    TripService(TripRepository repository){
        this.repository = repository;
    }

    List<Trip> getAll() {
      return repository.findAll();
    }

    List<Trip> getAllActive() {
      return repository.findAllActiveTrips();
    }

    public void updateHotelsRooms(JSONObject jsonObject){

      JSONArray listIds = jsonObject.getJSONArray("trip_offers_id");
      String operationType = jsonObject.getString("operation_type");
      String roomType =  jsonObject.getString("room_type");

      for (int i=0; i < listIds.length(); i++) {
        String id = listIds.getString(i);
        Optional<Trip> tripOpt = repository.findById(id);
        if (tripOpt.isPresent()){
          Trip trip = tripOpt.get();
          int freeSeats = trip.getHotel().getRooms().get(roomType).getAvailable();
        if (operationType.equals("add")){
          freeSeats++;
        }else{
          freeSeats--;
        }
        trip.getHotel().getRooms().get(roomType).setAvailable(freeSeats);
        repository.save(trip);
        }
      } 
    }

    public void updateTripStatus(JSONObject jsonObject){

      JSONArray listIds = jsonObject.getJSONArray("trip_offers_id");
      boolean isHotelBookedUp =  jsonObject.getBoolean("is_hotel_booked_up");

      for (int i=0; i < listIds.length(); i++) {
        String id = listIds.getString(i);
        Optional<Trip> tripOpt = repository.findById(id);
        if (tripOpt.isPresent()){
          Trip trip = tripOpt.get();
          trip.setBookedUp(isHotelBookedUp);
          repository.save(trip);
        }
      } 
    }

    Trip getbyId(String id) {
      return repository.findByTripID(id);
  }
}
