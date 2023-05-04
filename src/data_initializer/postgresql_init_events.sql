CREATE TABLE EventsLog
(
    ID          SERIAL PRIMARY KEY,
    Type        varchar(50),
    Operation   varchar(50),
    "From"      varchar(50),
	"To"		varchar(50),
    ReceiveDate timestamp,
    Body        json
);
