package handler

import (
	"encoding/json"
	db "event_hub_ms_v2/database"
	events "event_hub_ms_v2/events"
	"fmt"
	"log"

	"github.com/streadway/amqp"
)

type TransportHandler struct {
	DbHandler          *db.DatabaseHandler
	channel            *amqp.Channel
	ReservationHandler *ReservationHandler
}

func (transport *TransportHandler) Initialize() {
	conn, err := amqp.Dial("amqp://admin:admin@rabbitmq:5672//victor_travels")
	failOnError(err, "Failed to connect to RabbitMQ")

	ch, err := conn.Channel()
	transport.channel = ch
	failOnError(err, "Failed to open a channel")

	q, err := ch.QueueDeclare(
		"transport-events-for-eventhub-ms", // queque name
		true,                               // durable
		false,                              // autoDelete
		false,                              // exclusive
		false,                              // noWait
		nil,                                // arguments
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
		fmt.Printf("Received Message from TransportMS queque: %s\n", msg.Body)

		var transportEvent events.TransportEvent
		err := json.Unmarshal([]byte(msg.Body), &transportEvent)
		if err != nil {
			log.Printf("Error decoding JSON: %v\n", err)
			return
		}
		transport.DbHandler.SaveTransportEvent(transportEvent)
		transport.ReservationHandler.sendMessageFromTransport(transportEvent)
	}

}

func (transport *TransportHandler) PrepareGeneratedEventMessage(randomEvent events.RandomGeneratedEvent) {
	title := "generated_transport_update"
	operationType := randomEvent.Operation
	value := randomEvent.Value
	connectionId := randomEvent.Name
	resourceType := randomEvent.Resource
	transportEventDTO := events.TransportGeneratedDTO{Title: title, OperationType: operationType, Value: value, ConnectionId: connectionId, ResourceType: resourceType}
	transport.DbHandler.SaveTransportGeneratedEventDTO(transportEventDTO)
	transport.sendTransportGeneratedMessage(transportEventDTO)
}

func (transport *TransportHandler) PrepareReservationEventMessage(randomEvent events.ReservationEvent) {
	title := "trip_offer_transport_update"
	tripOfferId := randomEvent.TripOfferId
	connectionIdTo := randomEvent.ConnectionIdTo
	connectionIdFrom := randomEvent.ConnectionIdFrom
	headCount := randomEvent.HeadCount
	var operationType string
	if randomEvent.ReservationStatus == "created" {
		operationType = "delete"
	} else {
		operationType = "add"
	}

	transportEventDTO := events.TransportDTO{Title: title, TripOfferId: tripOfferId, ConnectionIdTo: connectionIdTo, ConnectionIdFrom: connectionIdFrom, HeadCount: headCount, OperationType: operationType}
	transport.DbHandler.SaveTransportEventDTO(transportEventDTO)
	transport.sendMessage(transportEventDTO)
}

func (transport *TransportHandler) sendMessage(object events.TransportDTO) {
	body, _ := json.Marshal(object)
	_, err := transport.channel.QueueDeclare(
		"transport-events-for-transport-ms", // queque name
		true,                                // durable
		false,                               // autoDelete
		false,                               // exclusive
		false,                               // noWait
		nil,                                 // arguments
	)
	failOnError(err, "Failed to declare a queue")

	transport.channel.Publish(
		"transport-events",                  // Exchange
		"transport-events-for-transport-ms", // Routing key
		false,                               // Mandatory
		false,                               // Immediate
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        body,
		},
	)
	fmt.Printf("Send Message to transportMS: %s\n", body)
}
func (transport *TransportHandler) sendTransportGeneratedMessage(object events.TransportGeneratedDTO) {
	body, _ := json.Marshal(object)
	_, err := transport.channel.QueueDeclare(
		"transport-events-for-transport-ms", // queque name
		true,                                // durable
		false,                               // autoDelete
		false,                               // exclusive
		false,                               // noWait
		nil,                                 // arguments
	)
	failOnError(err, "Failed to declare a queue")

	transport.channel.Publish(
		"transport-events",                  // Exchange
		"transport-events-for-transport-ms", // Routing key
		false,                               // Mandatory
		false,                               // Immediate
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        body,
		},
	)
	fmt.Printf("Send Message to transportMS: %s\n", body)
}
