## Dokumentacja Queues and exchanges w RabbitMQ VictorTravels

> Queue - miejsce z którego zjadamy wiadomość (consume)

> Exchange - miejsce do którego wrzucamy naszą wiadomość (publish)

### Co trzeba wiedzieć konsumując z kolejki?

    "vhost": "/victor_travels", - Nazwe vhosta(wszędzie jest taka sama)
    "destination": "databaseUpdatesQueue", - nazwę kolejki

### Co trzeba wiedzieć publikując do kolejki?

      "source": "databaseUpdatesExchange", - Nazwę exchanga
      "vhost": "/victor_travels", - Nazwe vhosta(wszędzie jest taka sama)
      "routing_key": "databaseUpdatesQueue" - wartość routing key, które jest zawsze taka sama jak nazwa kolejki przypiętej do exchanga

---
Opisane wyżej przykłady są wyjęte z pliku `definitions.json`, gdzie znajdują się szczegóły wszystkich kolejek i
exchangy.