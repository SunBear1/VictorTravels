CREATE TABLE EventsLog
(
    ID          SERIAL PRIMARY KEY,
    Type        varchar(50),
    Operation   varchar(50),
    "From"      varchar(50),
    ReceiveDate timestamp,
    Body        json
);
INSERT INTO EventsLog (Type, Operation, "From", ReceiveDate, Body)
VALUES ('ReservationStatusUpdate', 'created', 'ReservationMS', '2023-04-27 17:22:10', '{
  "trip_offer_id": "1234",
  "reservation_status": "created"
}');
