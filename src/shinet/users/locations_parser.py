"""
This module contains functions for parsing Russian cities
"""
from __future__ import annotations

import logging
import requests
import json
from bs4 import BeautifulSoup
from typing import List, Tuple
from re import match

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


def _get_districts_url(city_name: str) -> str | None:
    url = f'https://ru.wikipedia.org/wiki/{city_name}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        if match('Административное деление.*$', link.text):
            return f'https://ru.wikipedia.org/wiki/{link.text}'
    return None


def get_districts(city_name: str) -> List[str]:
    districts_url = _get_districts_url(city_name)
    print(districts_url)
    if districts_url is not None:
        try:
            districts = []
            response = requests.get(districts_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            table_body = soup.find(class_='standard').find('tbody')
            table_rows = table_body.find_all('tr')
            for tr in table_rows:
                tds = tr.find_all('td')
                try:
                    district_name = tds[1].find('a').text
                    districts.append(district_name.split()[0])
                except:
                    ...
            return districts
        except:
            return []
    return []


if __name__ == '__main__':
    districts = dict()
    cities = get_cities_list()
    try:
        for city in cities:
            districts[city] = get_districts(city)
            print(f'{city} parsed')
        with open('cities.json', 'w') as f:
            json.dump(districts, f, ensure_ascii=False,)
    except Exception as e:
        print(e)
        with open('cities.json', 'w') as f:
            json.dump(districts, f, ensure_ascii=False,)



