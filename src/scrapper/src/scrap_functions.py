import random

import bs4.element


def create_trip_dict(hotel_core_info_html: bs4.element.ResultSet, dep_locations: list, hotel_imgs: list,
                     hotel_desc: list) -> dict:
    base_trips = dict()
    for element in hotel_core_info_html:
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
                            base_trips[hotel_name]["from"] = sorted(
                                random.sample(dep_locations, random.randint(4, len(dep_locations) - 3)))
                            base_trips[hotel_name]["description"] = list()
                            for k in range(4):
                                base_trips[hotel_name]["description"].append(hotel_desc.pop(0))

                            for hotel in hotel_imgs:
                                if hotel[0] == hotel_name:
                                    base_trips[hotel_name]["img"] = hotel[1]
                                    break
                            break
    return base_trips


def get_hotel_descriptions(hotel_desc_html: bs4.element.ResultSet) -> list:
    hotel_descriptions = []
    for hotel_desc in hotel_desc_html:
        [hotel_descriptions.append(desc.text) for desc in hotel_desc.contents]
    return hotel_descriptions


def get_hotel_images(hotel_img_html: bs4.element.ResultSet) -> list:
    hotel_images = list()
    for i in range(0, len(hotel_img_html), 2):
        hotel_images.append((hotel_img_html[i]["alt"], hotel_img_html[i]["src"]))

    return list(hotel_images)


def get_departure_locations(dep_regions_html: bs4.element.ResultSet) -> list:
    example_dep_locations_html = dep_regions_html[0]
    departure_locations = list()
    [departure_locations.append(city_name.text) for city_name in example_dep_locations_html]
    return departure_locations
