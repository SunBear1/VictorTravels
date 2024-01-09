package main

import (
	"database/sql"
	"log"
	"time"

	_ "github.com/lib/pq"
	"github.com/streadway/amqp"

	database "event_hub_ms_v2/database"
	handlers "event_hub_ms_v2/handler"
)

func main() {
	var db *sql.DB
	var err error

	println("Event hub v2 is starting.. ")
	connStr := "postgres://postgres:student@postgresql/rsww_17998_events?sslmode=disable"
	// Connect to database
	for {
		db, err = sql.Open("postgres", connStr)
		if err != nil {
			log.Println("Error connecting to the database:", err)
			time.Sleep(time.Second * 5)
		} else {
			break
		}
	}

	if db == nil {
		log.Fatal("Failed to establish a database connection.")
	}
	for {
		_, err := amqp.Dial("amqp://admin:admin@rabbitmq:5672//victor_travels")
		if err != nil {
			log.Println("Failed to connect to RabbitMQ:")
			time.Sleep(time.Second * 5)
		} else {
			break
		}
	}

	databaseHandler := &database.DatabaseHandler{Db: db}               // Utwórz wskaźnik do DatabaseHandler
	HotelHandler := &handlers.HotelHandler{DbHandler: databaseHandler} // Utwórz wskaźnik do DatabaseHandler
	ReservationHandler := &handlers.ReservationHandler{DbHandler: databaseHandler}
	TransportHandler := &handlers.TransportHandler{DbHandler: databaseHandler}
	LiveEventHandler := &handlers.LiveEventsHandler{DbHandler: databaseHandler}

	ReservationHandler.HotelHandler = HotelHandler
	HotelHandler.ReservationHandler = ReservationHandler
	TransportHandler.ReservationHandler = ReservationHandler
	LiveEventHandler.ReservationHandler = ReservationHandler
	ReservationHandler.LiveEventsHandler = LiveEventHandler
	ReservationHandler.TransportHandler = TransportHandler

	go HotelHandler.Initialize()
	go ReservationHandler.Initialize()
	go TransportHandler.Initialize()
	go LiveEventHandler.Initialize()

	randomGeneratedEvent := &handlers.GeneratedEventsHandler{DbHandler: databaseHandler, HotelHandler: HotelHandler, TransportHandler: TransportHandler, LiveEventsHandler: LiveEventHandler}
	go randomGeneratedEvent.Initialize()

	// Utwórz kanał, który nie będzie używany, ale pozwoli na używanie select{}
	stopChan := make(chan struct{})

	// Ta pętla będzie utrzymywać główny wątek w działaniu
	select {
	case <-stopChan:
		// Ta linia nigdy nie zostanie wykonana, bo nie zamykamy stopChan
	}
}
