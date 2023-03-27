import random

import bs4.element


def create_base_trip_dict(html_from_source: bs4.element.ResultSet) -> dict:
    base_trips = dict()
    for element in html_from_source:
        for i in range(len(element.contents) - 1):
            for details in reversed(element.contents[i + 1].contents):
                if details.text:
                    hotel_name = details.text
                    hotel_country = element.contents[i].contents[0].text.strip(" / ")
                    for j in range(1, len(element.contents[i].contents)):
                        if element.contents[i].contents[j].text.strip(" / "):
                            hotel_region = element.contents[i].contents[j].text.strip(" / ")
                            parts = hotel_region.split("/")
                            if len(parts) > 1:
                                hotel_region = parts[1].strip()
                            base_trips[hotel_name] = {
                                "localisation": {
                                    "country": hotel_country,
                                    "region": hotel_region
                                }
                            }
                            break
    return base_trips


def create_locations_list(html_from_source: bs4.element.ResultSet) -> list:
    departure_locations = list()
    [departure_locations.append(city_name.text) for city_name in html_from_source]
    return departure_locations


def fill_trips_with_departure_locations(departure_locations: list, trips: dict) -> dict:
    for trip in trips.values():
        dep_locs_number = random.randint(4, len(departure_locations) - 3)
        trip["from"] = sorted(random.sample(departure_locations, dep_locs_number))
    return trips
