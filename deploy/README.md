# Instrukcja Obłsugi Makefile'a

`make build` - Buduje wszystkie obrazy

`make run` - Odpala docker compose up, czyli stawia wszystkie kontenery

`make clean` - Czyści wszystkie obrazy

`make gateway - Buduje tylko obraz gateway'a

`make rabbit` - Buduje tylko obraz rabbit'a

itd itd....

szczegóły w Makefilu

## Porty

- 17998 - RabbitMQ(**AMQP**)
- 17999 - Trip researcher
- 18000 - Gateway
- 18001 - Reservations MS
- 18002 - Purchase MS
- 18003 - Payments MS
- 18004 - RabbitMQ(**UI**)

