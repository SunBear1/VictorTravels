package handler

import (
	"encoding/json"
	db "event_hub_ms_v2/database"
	events "event_hub_ms_v2/events"
	"fmt"
	"log"

	"github.com/streadway/amqp"
)

type GeneratedEventsHandler struct {
	DbHandler        *db.DatabaseHandler
	HotelHandler     *HotelHandler
	TransportHandler *TransportHandler
}

func (generatedEventsHandler *GeneratedEventsHandler) Initialize() {
	conn, err := amqp.Dial("amqp://admin:admin@rabbitmq:5672//victor_travels")
	failOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"generated-random-events-for-eventhub-ms", // queque name
		true,  // durable
		false, // autoDelete
		false, // exclusive
		false, // noWait
		nil,   // arguments
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

	// print consumed messages from queue
	forever := make(chan bool)
	go func() {
		for msg := range msgs {
			fmt.Printf("Received Message: %s\n", msg.Body)
			var randomGeneratedEvent events.RandomGeneratedEvent
			err := json.Unmarshal([]byte(msg.Body), &randomGeneratedEvent)
			if err != nil {
				log.Printf("Error decoding JSON: %v\n", err)
				return
			}
			generatedEventsHandler.DbHandler.SaveRandomGeneratedEvent(randomGeneratedEvent)

			if randomGeneratedEvent.Type == "hotel" {
				generatedEventsHandler.HotelHandler.PrepareGeneratedEventMessage(randomGeneratedEvent)
			}
			if randomGeneratedEvent.Type == "connection" {
				generatedEventsHandler.TransportHandler.PrepareGeneratedEventMessage(randomGeneratedEvent)
			}
			//TODO liveEventsMQ.sendRandomGeneratedEventMessage(randomGeneratedEvent)
		}
	}()

	fmt.Println("Waiting for messages...")
	<-forever
}
