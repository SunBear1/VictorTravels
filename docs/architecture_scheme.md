# Ogólna architektura systemu

![Architektura systemu.png](architecture.jpg)


- **REST** - Serwisy komunikują się protokołem HTTP
- **AMQP** - Serwisy komunikują się z kolejką RabbitMQ za pomocą protokołu AMQP
- **SYMBOL SZCZEŚCIANU** - Jeden serwis biznesowy
- **SYMBOL WALCA** - Jedna baza danych. Może być bezpośrednio związana z danym serwisem.
- **SYMBOL DWÓCH STRZAŁEK** - Jedna kolejka w RabbitMQ.
---
## Lista serwisów w systemie

- GUI - warstwa prezentacji, czyli frontend.
- USER_HANDLER - serwis odpowiedzialny za uwierzytelnienie użytkowników.
- DIRECTOR_MS - serwis odpowiedzialny za komunikację z TO oraz za komunikację z frontendem. Posiada on główną "czystą" bazę danych wycieczek.
- TOUR_RESEARCHER_MS - serwis odpowiedzialny za wyszukiwanie i listowanie wycieczek dla klienta.
- RESERVATIONS_MS -  serwis odpowiedzialny za obsługę reserwacji. Serwis ten księguje oraz obsługuje operacje kupna wycieczki.
- PURCHASE_MS -  serwis odpowiedzialny za obsługę kupna wycieczki. Serwis ten księguje oraz obsługuje operacje kupna wycieczki.
- PAYMENT_MS - serwis odpowiedzialny za obsługę wpłat od klienta. Serwis ten symuluje przetwarzanie płatności, księguje je i losowo odrzuca płatność.

Większość serwisów będzie posiadała swoją własną bazę danych, z której będzie korzystała.