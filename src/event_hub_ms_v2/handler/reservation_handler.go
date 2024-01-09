package handler

import (
	"encoding/json"
	db "event_hub_ms_v2/database"
	events "event_hub_ms_v2/events"
	"fmt"
	"log"

	"github.com/streadway/amqp"
)

type ReservationHandler struct {
	DbHandler        *db.DatabaseHandler
	channel          *amqp.Channel
	HotelHandler     *HotelHandler
	TransportHandler *TransportHandler
}

func (reservation *ReservationHandler) Initialize() {
	conn, err := amqp.Dial("amqp://admin:admin@rabbitmq:5672//victor_travels")
	failOnError(err, "Failed to connect to RabbitMQ")

	ch, err := conn.Channel()
	reservation.channel = ch
	failOnError(err, "Failed to open a channel")

	q, err := ch.QueueDeclare(
		"reservations-for-eventhub-ms", // queque name
		true,                           // durable
		false,                          // autoDelete
		false,                          // exclusive
		false,                          // noWait
		nil,                            // arguments
	)
	failOnError(err, "Failed to declare a queue")

	// Rozpocznij konsumpcję wiadomości w osobnej gorutynie
	msgs, err := ch.Consume(
		q.Name, // queque name
		"",     // pusty consumer tag
		true,   // autoAck - potwierdzaj automatycznie
		false,  // exclusive
		false,  // noLocal
		false,  // noWait
		nil,    // arguments
	)
	failOnError(err, "Failed to register a consumer")

	for msg := range msgs {
		fmt.Printf("Received Message: %s\n", msg.Body)

		var reservationEvent events.ReservationEvent
		err := json.Unmarshal([]byte(msg.Body), &reservationEvent)
		if err != nil {
			log.Printf("Error decoding JSON: %v\n", err)
			return
		}
		reservation.DbHandler.SaveReservationEvent(reservationEvent)

		if reservationEvent.ReservationStatus != "finalized" {
			if reservationEvent.ReservationStatus != "created" {
				tmp := reservation.DbHandler.GetReservationById(reservationEvent.ReservationId)
				reservationEvent.HotelId = tmp.HotelId
				reservationEvent.RoomType = tmp.RoomType
				reservationEvent.ConnectionIdFrom = tmp.ConnectionIdFrom
				reservationEvent.ConnectionIdTo = tmp.ConnectionIdTo
				reservationEvent.HeadCount = tmp.HeadCount
			}
			reservation.HotelHandler.PrepareReservationEventMessage(reservationEvent)
			reservation.TransportHandler.PrepareReservationEventMessage(reservationEvent)
		}
		if reservationEvent.ReservationStatus == "created" || reservationEvent.ReservationStatus == "finalized" {
			// TODO	liveEventsMQ.sendReservationEventMessage(reservationEvent);

		}

	}

}

func (reservation *ReservationHandler) sendMessageFromHotel(hotelEvent events.HotelEvent) {
	_, err := reservation.channel.QueueDeclare(
		"reservations-for-reservations-ms", // queque name
		true,                               // durable
		false,                              // autoDelete
		false,                              // exclusive
		false,                              // noWait
		nil,                                // arguments
	)
	failOnError(err, "Failed to declare a queue")

	title := hotelEvent.Title
	tripOffersAffected := hotelEvent.TripOffersId
	var operationType string
	if hotelEvent.IsHotelBookedUp {
		operationType = "delete"
	} else {
		operationType = "add"
	}
	reservationDTO := events.ReservationDTO{Title: title, TripOffersAffected: tripOffersAffected, OperationType: operationType}
	reservation.DbHandler.SaveReservationDTO(reservationDTO)
	body, _ := json.Marshal(reservationDTO)
	reservation.channel.Publish(
		"reservations",                     // Exchange
		"reservations-for-reservations-ms", // Routing key
		false,                              // Mandatory
		false,                              // Immediate
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        body,
		},
	)
	fmt.Printf("Send Message to reservationMS: %s\n", body)
}

func (reservation *ReservationHandler) sendMessageFromTransport(transportEvent events.TransportEvent) {
	_, err := reservation.channel.QueueDeclare(
		"reservations-for-reservations-ms", // queque name
		true,                               // durable
		false,                              // autoDelete
		false,                              // exclusive
		false,                              // noWait
		nil,                                // arguments
	)
	failOnError(err, "Failed to declare a queue")

	title := transportEvent.Title
	tripOffersAffected := transportEvent.TripOffersId
	var operationType string
	if transportEvent.IsTransportBookedUp {
		operationType = "delete"
	} else {
		operationType = "add"
	}
	connectionId := transportEvent.ConnectionId
	reservationDTO := events.ReservationDTO{Title: title, TripOffersAffected: tripOffersAffected, OperationType: operationType, ConnectionId: connectionId}
	reservation.DbHandler.SaveReservationDTO(reservationDTO)
	body, _ := json.Marshal(reservationDTO)
	reservation.channel.Publish(
		"reservations",                     // Exchange
		"reservations-for-reservations-ms", // Routing key
		false,                              // Mandatory
		false,                              // Immediate
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        body,
		},
	)
	fmt.Printf("Send Message to reservationMS: %s\n", body)
}
