package handler

import (
	"encoding/json"
	db "event_hub_ms_v2/database"
	events "event_hub_ms_v2/events"
	"fmt"
	"log"

	"github.com/streadway/amqp"
)

type HotelHandler struct {
	DbHandler          *db.DatabaseHandler
	channel            *amqp.Channel
	ReservationHandler *ReservationHandler
}

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

func (hotel *HotelHandler) Initialize() {
	conn, err := amqp.Dial("amqp://admin:admin@rabbitmq:5672//victor_travels")
	failOnError(err, "Failed to connect to RabbitMQ")

	ch, err := conn.Channel()
	hotel.channel = ch
	failOnError(err, "Failed to open a channel")

	q, err := ch.QueueDeclare(
		"hotel-events-for-eventhub-ms", // queque name
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
		fmt.Printf("Received Message from HotelMS queque: %s\n", msg.Body)

		var hotelEvent events.HotelEvent
		err := json.Unmarshal([]byte(msg.Body), &hotelEvent)
		if err != nil {
			log.Printf("Error decoding JSON: %v\n", err)
			return
		}
		hotel.DbHandler.SaveHotelEvent(hotelEvent)
		hotel.ReservationHandler.sendMessageFromHotel(hotelEvent)
	}

}

func (hotel *HotelHandler) PrepareGeneratedEventMessage(randomEvent events.RandomGeneratedEvent) {
	title := "trip_offer_hotel_room_update"
	operationType := randomEvent.Operation
	hotelId := randomEvent.Name
	roomType := randomEvent.Field
	resourceAmount := randomEvent.Value
	resourceType := randomEvent.Resource
	tripOfferId := hotel.DbHandler.GetTripOfferIdByHotelId(hotelId)
	hotelEventDTO := events.HotelEventDTO{Title: title, TripOfferId: tripOfferId, OperationType: operationType, HotelId: hotelId,
		RoomType: roomType, ResourceAmount: resourceAmount, ResourceType: resourceType}
	hotel.DbHandler.SaveHotelEventDTO(hotelEventDTO)
	hotel.sendMessage(hotelEventDTO)
}

func (hotel *HotelHandler) PrepareReservationEventMessage(randomEvent events.ReservationEvent) {
	title := "trip_offer_hotel_room_update"
	tripOfferId := randomEvent.TripOfferId
	hotelId := randomEvent.HotelId
	roomType := randomEvent.RoomType
	resourceAmount := 1
	resourceType := "availability"

	var operationType string
	if randomEvent.ReservationStatus == "created" {
		operationType = "delete"
	} else {
		operationType = "add"
	}

	hotelEventDTO := events.HotelEventDTO{Title: title, TripOfferId: tripOfferId, OperationType: operationType, HotelId: hotelId,
		RoomType: roomType, ResourceAmount: resourceAmount, ResourceType: resourceType}
	hotel.DbHandler.SaveHotelEventDTO(hotelEventDTO)
	hotel.sendMessage(hotelEventDTO)
}

func (hotel *HotelHandler) sendMessage(object events.HotelEventDTO) {
	body, _ := json.Marshal(object)
	_, err := hotel.channel.QueueDeclare(
		"hotel-events-for-hotel-ms", // queque name
		true,                        // durable
		false,                       // autoDelete
		false,                       // exclusive
		false,                       // noWait
		nil,                         // arguments
	)
	failOnError(err, "Failed to declare a queue")

	hotel.channel.Publish(
		"hotel-events",              // Exchange
		"hotel-events-for-hotel-ms", // Routing key
		false,                       // Mandatory
		false,                       // Immediate
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        body,
		},
	)
	fmt.Printf("Send Message to hotelMS: %s\n", body)
}
