package events

type HotelEvent struct {
	Title           string
	TripOffersId    []string
	IsHotelBookedUp bool
}

type HotelEventDTO struct {
	Title          string `json:"title"`
	TripOfferId    string `json:"trip_offer_id"`
	OperationType  string `json:"operation_type"`
	HotelId        string `json:"hotel_id"`
	RoomType       string `json:"room_type"`
	ResourceAmount int    `json:"resource_amount"`
	ResourceType   string `json:"resource_type"`
}

type RandomGeneratedEvent struct {
	Title     string
	Type      string
	Name      string
	Field     string
	Resource  string
	Value     int
	Operation string
	Id        int
}

type ReservationEvent struct {
	Title             string
	TripOfferId       string
	ReservationId     string
	ReservationStatus string
	HotelId           string
	RoomType          string
	ConnectionIdTo    string
	ConnectionIdFrom  string
	HeadCount         int
}
type ReservationDTO struct {
	Title              string   `json:"title"`
	OperationType      string   `json:"operation_type"`
	ConnectionId       string   `json:"connection_id"`
	TripOffersAffected []string `json:"trip_offers_affected"`
}

type TransportEvent struct {
	Title               string
	TripOffersId        []string
	ConnectionId        string
	IsTransportBookedUp bool
}

type TransportDTO struct {
	Title            string `json:"title"`
	TripOfferId      string `json:"trip_offer_id"`
	ConnectionIdTo   string `json:"connection_id_to"`
	ConnectionIdFrom string `json:"connection_id_from"`
	HeadCount        int    `json:"head_count"`
	OperationType    string `json:"operation_type"`
}

type TransportGeneratedDTO struct {
	Title         string `json:"title"`
	ConnectionId  string `json:"connection_id"`
	ResourceType  string `json:"resource_type"`
	Value         int    `json:"value"`
	OperationType string `json:"operation_type"`
}
