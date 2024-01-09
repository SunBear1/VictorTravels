package database

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"time"

	events "event_hub_ms_v2/events"

	_ "github.com/lib/pq"
)

type DatabaseHandler struct {
	Db *sql.DB
}

func (db *DatabaseHandler) SaveEvent(eventType string, operation string, from string, to string, receiveDate time.Time, json string) {
	timeStamp := receiveDate.Format("2006-01-02 15:04:05")

	query := "INSERT INTO eventslog (Type, Operation, \"From\", \"To\", ReceiveDate, Body) VALUES ($1, $2, $3, $4, $5, $6)"
	db.Db.Exec(query, eventType, operation, from, to, timeStamp, json)
}

func (db *DatabaseHandler) SaveRandomGeneratedEvent(randomEvent events.RandomGeneratedEvent) {
	timeStamp := time.Now()
	from := "EventGenerator"
	to := "EventhubMS"
	operation := randomEvent.Operation
	eventType := randomEvent.Title
	jsonData, err := json.Marshal(randomEvent)
	if err != nil {
		fmt.Println("Error marshalling JSON:", err)
		return
	}
	db.SaveEvent(eventType, operation, from, to, timeStamp, string(jsonData))
}

func (db *DatabaseHandler) SaveHotelEvent(hotelEvent events.HotelEvent) {
	timeStamp := time.Now()
	from := "HotelMS"
	to := "EventhubMS"
	operation := ""
	if hotelEvent.IsHotelBookedUp {
		operation = "delete"
	} else {
		operation = "add"
	}
	eventType := hotelEvent.Title
	jsonData, err := json.Marshal(hotelEvent)
	if err != nil {
		fmt.Println("Error marshalling JSON:", err)
		return
	}
	db.SaveEvent(eventType, operation, from, to, timeStamp, string(jsonData))
}

func (db *DatabaseHandler) SaveReservationEvent(reservationEvent events.ReservationEvent) {
	timeStamp := time.Now()
	from := "ReservationMS"
	to := "EventhubMS"
	operation := ""
	if reservationEvent.ReservationStatus == "created" {
		operation = "delete"
	} else {
		operation = "add"
	}
	eventType := reservationEvent.Title
	jsonData, err := json.Marshal(reservationEvent)
	if err != nil {
		fmt.Println("Error marshalling JSON:", err)
		return
	}
	db.SaveEvent(eventType, operation, from, to, timeStamp, string(jsonData))
}

func (db *DatabaseHandler) SaveTransportEvent(transportEvent events.TransportEvent) {
	timeStamp := time.Now()
	from := "TransportMS"
	to := "EventhubMS"
	operation := ""
	if transportEvent.IsTransportBookedUp {
		operation = "delete"
	} else {
		operation = "add"
	}
	eventType := transportEvent.Title
	jsonData, err := json.Marshal(transportEvent)
	if err != nil {
		fmt.Println("Error marshalling JSON:", err)
		return
	}
	db.SaveEvent(eventType, operation, from, to, timeStamp, string(jsonData))
}

func (db *DatabaseHandler) SaveHotelEventDTO(hotelEvent events.HotelEventDTO) {
	timeStamp := time.Now()
	to := "HotelMS"
	from := "EventhubMS"
	operation := hotelEvent.OperationType
	eventType := hotelEvent.Title
	jsonData, err := json.Marshal(hotelEvent)
	if err != nil {
		fmt.Println("Error marshalling JSON:", err)
		return
	}
	db.SaveEvent(eventType, operation, from, to, timeStamp, string(jsonData))
}

func (db *DatabaseHandler) SaveTransportEventDTO(transportEvent events.TransportDTO) {
	timeStamp := time.Now()
	to := "TransportMS"
	from := "EventhubMS"
	operation := transportEvent.OperationType
	eventType := transportEvent.Title
	jsonData, err := json.Marshal(transportEvent)
	if err != nil {
		fmt.Println("Error marshalling JSON:", err)
		return
	}
	db.SaveEvent(eventType, operation, from, to, timeStamp, string(jsonData))
}

func (db *DatabaseHandler) SaveTransportGeneratedEventDTO(transportEvent events.TransportGeneratedDTO) {
	timeStamp := time.Now()
	to := "TransportMS"
	from := "EventhubMS"
	operation := transportEvent.OperationType
	eventType := transportEvent.Title
	jsonData, err := json.Marshal(transportEvent)
	if err != nil {
		fmt.Println("Error marshalling JSON:", err)
		return
	}
	db.SaveEvent(eventType, operation, from, to, timeStamp, string(jsonData))
}

func (db *DatabaseHandler) SaveReservationDTO(hotelEvent events.ReservationDTO) {
	timeStamp := time.Now()
	to := "EventhubMS"
	from := "ReservationMS"
	operation := hotelEvent.OperationType
	eventType := hotelEvent.Title
	jsonData, err := json.Marshal(hotelEvent)
	if err != nil {
		fmt.Println("Error marshalling JSON:", err)
		return
	}
	db.SaveEvent(eventType, operation, from, to, timeStamp, string(jsonData))
}

func (db *DatabaseHandler) GetTripOfferIdByHotelId(hotelId string) string {
	query := "SELECT offerid FROM tripsforliveevents WHERE hotelid = '" + hotelId + "';"
	rows, _ := db.Db.Query(query)
	for rows.Next() {
		var offerID string
		rows.Scan(&offerID)
		return offerID
	}
	return ""
}

func (db *DatabaseHandler) GetReservationById(id string) events.ReservationEvent {
	query := "SELECT body FROM eventslog WHERE \"From\" = $1 AND body->>'reservation_id' = $2 "
	rows, _ := db.Db.Query(query, "ReservationMS", id)
	for rows.Next() {
		var body string
		var event events.ReservationEvent
		rows.Columns()
		rows.Scan(&body)
		json.Unmarshal([]byte(body), &event)
		return event
	}
	return events.ReservationEvent{}
}

func (db *DatabaseHandler) GetTripById(id string) events.LiveEventDTO {
	query := "SELECT tripid,hotelname,country,region FROM eventslog WHERE offerid = $1"
	rows, _ := db.Db.Query(query, id)
	for rows.Next() {
		var tripID int
		var hotelName string
		var country string
		var region string
		rows.Scan(&tripID, &hotelName, &country, &region)
		return events.LiveEventDTO{TripId: tripID, HotelName: hotelName, Country: country, Region: region}
	}
	return events.LiveEventDTO{}
}
