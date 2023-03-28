import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.scrapper.src.scrap_functions import create_trip_dict, get_departure_locations, \
    get_hotel_descriptions, get_hotel_images

ITAKA_URL = "https://www.itaka.pl/wyniki-wyszukiwania/wakacje/?view=offerList&package-type=wczasy&adults=2&order=popular&total-price=0&page=1&currency=PLN"
CHROME_DRIVER_PATH = "../dependencies/chromedriver.exe"

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
driver.get(url=ITAKA_URL)
body = driver.find_element(By.TAG_NAME, 'body')
for i in range(8):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.4)
html_source = driver.page_source
driver.quit()

itaka_src = BeautifulSoup(html_source, "html.parser")

hotel_description_elements = itaka_src.find_all("ul", class_="offer_assets")
hotel_descriptions = get_hotel_descriptions(hotel_desc_html=hotel_description_elements)

hotel_image_elements = itaka_src.find_all("img", class_="figure_main-photo")
hotel_images = get_hotel_images(hotel_img_html=hotel_image_elements)

dep_region_elements = itaka_src.select("div.dep-region_list.clearfix.undefined")
departure_locations = get_departure_locations(dep_regions_html=dep_region_elements)

hotel_core_info_elements = itaka_src.find_all("header", class_="offer_header")
trips = create_trip_dict(hotel_core_info_html=hotel_core_info_elements, dep_locations=departure_locations,
                         hotel_imgs=hotel_images,
                         hotel_desc=hotel_descriptions)

with open("../trips_json.json", "w", encoding="utf-8") as output:
    json.dump(trips, output, indent=4, ensure_ascii=False)

print(trips)
