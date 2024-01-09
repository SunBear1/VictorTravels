package handler

import (
	"encoding/json"
	db "event_hub_ms_v2/database"
	events "event_hub_ms_v2/events"
	"fmt"
	"regexp"
	"strings"
	"time"

	"github.com/streadway/amqp"
)

type LiveEventsHandler struct {
	DbHandler          *db.DatabaseHandler
	channel            *amqp.Channel
	ReservationHandler *ReservationHandler
}

func (liveEvents *LiveEventsHandler) Initialize() {
	conn, err := amqp.Dial("amqp://admin:admin@rabbitmq:5672//victor_travels")
	failOnError(err, "Failed to connect to RabbitMQ")

	ch, err := conn.Channel()
	liveEvents.channel = ch
	failOnError(err, "Failed to open a channel")

	_, err = ch.QueueDeclare(
		"live-events-for-gateway", // queque name
		true,                      // durable
		false,                     // autoDelete
		false,                     // exclusive
		false,                     // noWait
		nil,                       // arguments
	)
	failOnError(err, "Failed to declare a queue")
	for {
		time.Sleep(250 * time.Millisecond)
	}
}

func extractTransportType(input string) string {
	re := regexp.MustCompile(`-(TRAIN|PLANE)-`)
	matches := re.FindStringSubmatch(input)

	if len(matches) > 1 {
		extracted := matches[1]
		return strings.ToLower(extracted)
	}

	return ""
}

func (liveEvent *LiveEventsHandler) sendRandomGeneratedMessage(object events.RandomGeneratedEvent) {
	body, _ := json.Marshal(object)

	liveEvent.channel.Publish(
		"live-events",             // Exchange
		"live-events-for-gateway", // Routing key
		false,                     // Mandatory
		false,                     // Immediate
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        body,
		},
	)
	fmt.Printf("Send Message to gatewayMS: %s\n", body)
}

func (liveEvent *LiveEventsHandler) sendReservationMessage(object events.ReservationEvent) {

	tripOfferId := object.TripOfferId
	roomType := object.RoomType
	connectionTo := object.ConnectionIdTo
	liveEventDTO := liveEvent.DbHandler.GetTripById(tripOfferId)
	liveEventDTO.RoomType = roomType
	liveEventDTO.TransportType = extractTransportType(connectionTo)

	body, _ := json.Marshal(liveEventDTO)

	liveEvent.channel.Publish(
		"live-events",             // Exchange
		"live-events-for-gateway", // Routing key
		false,                     // Mandatory
		false,                     // Immediate
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        body,
		},
	)
	fmt.Printf("Send Message to gatewayMS: %s\n", body)
}
