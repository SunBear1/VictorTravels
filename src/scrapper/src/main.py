import json

import requests
from bs4 import BeautifulSoup

from src.scrapper.src.scrap_functions import create_base_trip_dict, create_locations_list, \
    fill_trips_with_departure_locations

URL = "https://www.itaka.pl/wyniki-wyszukiwania/wakacje/?view=offerList&package-type=wczasy&adults=2&order=popular&total-price=0&page=1&currency=PLN"

itaka_src = BeautifulSoup(requests.get(URL).content, "html.parser")

with open("../data/departure_locations.html", mode="r", encoding="utf-8") as scrapper_html_src:
    local_src = BeautifulSoup(scrapper_html_src.read(), "html.parser")

offer_elements = itaka_src.find_all("header", class_="offer_header")
trips = create_base_trip_dict(html_from_source=offer_elements)

dep_region_elements = local_src.find_all('div', class_='dep-region_item')
departure_locations = create_locations_list(html_from_source=dep_region_elements)
trips = fill_trips_with_departure_locations(trips=trips, departure_locations=departure_locations)

print(len(trips))
json_trip_data = json.dumps(trips, indent=4, ensure_ascii=False).encode("utf-8")
print(json_trip_data.decode())
