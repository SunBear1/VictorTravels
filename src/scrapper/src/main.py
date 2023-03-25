import json

import requests
from bs4 import BeautifulSoup

from src.scrapper.src.scrap_functions import create_base_hotel_dict

URL = "https://www.itaka.pl/wyniki-wyszukiwania/wakacje/?view=offerList&package-type=wczasy&adults=2&order=popular&total-price=0&page=1&currency=PLN"

soup = BeautifulSoup(requests.get(URL).content, "html.parser")
offer_elements = soup.find_all("header", class_="offer_header")

trips = create_base_hotel_dict(html_from_source=offer_elements)

print(len(trips))
json_trip_data = json.dumps(trips, indent=4, ensure_ascii=False).encode("utf-8")
print(json_trip_data.decode())
