# Ogólna architektura systemu

![Architektura systemu.png](../diagrams/system_architecture_diagram.png)

## Lista serwisów w systemie

- GUI - warstwa prezentacji, czyli frontend.
- USER_HANDLER - serwis odpowiedzialny za uwierzytelnienie użytkowników.
- TOUR_RESEARCHER_MS - serwis odpowiedzialny za wyszukiwanie i listowanie wycieczek dla klienta.
- RESERVATIONS_MS - serwis odpowiedzialny za obsługę reserwacji. Serwis ten księguje oraz obsługuje operacje kupna
  wycieczki.
- PURCHASE_MS - serwis odpowiedzialny za obsługę kupna wycieczki. Serwis ten księguje oraz obsługuje operacje kupna
  wycieczki.
- PAYMENT_MS - serwis odpowiedzialny za obsługę wpłat od klienta. Serwis ten symuluje przetwarzanie płatności, księguje
  je i losowo odrzuca płatność.

Większość serwisów będzie posiadała swoją własną bazę danych, z której będzie korzystała.