import logging
import requests
import json
from bs4 import BeautifulSoup
from typing import List

logging.basicConfig(level=logging.INFO)

CITIES_LIST_URL = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8'


def get_cities_list() -> List[str]:
    response = requests.get(CITIES_LIST_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    cities = []
    tbody = soup.find('tbody')
    rows = tbody.find_all('tr')
    i = 0
    for row in rows:
        if i == 0:
            i += 1
            continue
        city_column = row.find_all('td')[2]
        city_name = city_column.find('a').text
        cities.append(city_name)
    return cities


if __name__ == '__main__':
    cities = get_cities_list()
    print(cities)




