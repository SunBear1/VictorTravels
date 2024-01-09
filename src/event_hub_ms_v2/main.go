package main

import (
	"database/sql"
	"log"
	"time"

	_ "github.com/lib/pq"

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

	databaseHandler := &database.DatabaseHandler{Db: db}               // Utwórz wskaźnik do DatabaseHandler
	HotelHandler := &handlers.HotelHandler{DbHandler: databaseHandler} // Utwórz wskaźnik do DatabaseHandler
	ReservationHandler := &handlers.ReservationHandler{DbHandler: databaseHandler}
	TransportHandler := &handlers.TransportHandler{DbHandler: databaseHandler}

	ReservationHandler.HotelHandler = HotelHandler
	HotelHandler.ReservationHandler = ReservationHandler
	TransportHandler.ReservationHandler = ReservationHandler

	go HotelHandler.Initialize()
	go ReservationHandler.Initialize()
	go TransportHandler.Initialize()

	randomGeneratedEvent := &handlers.GeneratedEventsHandler{DbHandler: databaseHandler, HotelHandler: HotelHandler, TransportHandler: TransportHandler}
	randomGeneratedEvent.Initialize()

	// Utwórz kanał, który nie będzie używany, ale pozwoli na używanie select{}
	stopChan := make(chan struct{})

	// Ta pętla będzie utrzymywać główny wątek w działaniu
	select {
	case <-stopChan:
		// Ta linia nigdy nie zostanie wykonana, bo nie zamykamy stopChan
	}
}
