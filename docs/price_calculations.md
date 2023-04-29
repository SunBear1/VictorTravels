# Algorytm obliczania ceny wycieczki

**Poszczególne grupy wiekowe płacą X procent regularnej ceny**

Dorośli:
- 100% podróż
- 100% hotel

Dzieci do lat 3:
- 0% podróż
- 10% hotel

Dzieci do lat 10:
- 50% podróż
- 50% hotel

Dzieci do lat 18:
- 60% podróż
- 70% hotelu

### Legenda
- CO - Cena kupna oferty od osoby 
- ZP - Zniżka na podróż dla osoby(inna w zależności od wieku) 
- ZH - Zniżka na noc hotelową dla osoby(inna w zależności od wieku)
- TDH - Cena transportu DO hotelu
- TZH - Cena transportu Z hotelu
- LN - Liczba noclegów
- CP - Cena pokoju za noc
- CD - Cena diety za posiłek
- P - prowizja od całości ceny

$$
  CO = \frac{ZP * (TDH + TZH) + LN * ZH * (CP + CD)}{P}
$$
