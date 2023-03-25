# Web scrapper wycieczek

Źródło - itaka.pl

### Co zbiera scrapper?

1. Hotel
    1. Zdjęcie
    2. Nazwa
    3. Opis
2. Skąd(miejsca wylotu)
3. Dokąd(lokalizacja hotelu)

```json
{
  "OsovaGrandHotel": {
    "image": "example_base64_photo",
    "description": [
      "Example description of a hotel"
    ],
    "from": [
      "Warszawa",
      "Kraków",
      "Gdańsk"
    ],
    "localisation": {
      "country": "France",
      "region": "Paris"
    }
  },
  "TorunExclusive": {
    "image": "example_base64_photo",
    "description": [
      "Example description of a hotel"
    ],
    "from": [
      "Wrocław",
      "Poznań"
    ],
    "localisation": {
      "country": "Greece",
      "region": "Crete"
    }
  }
}
```