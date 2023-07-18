"""
This module contains functions for parsing Russian cities
"""
from __future__ import annotations
import logging
import re

import requests
import json
from bs4 import BeautifulSoup
from typing import List, Tuple, Dict
from re import match, IGNORECASE


logging.basicConfig(level=logging.INFO)


REGIONS_URL = 'https://locdb.ru'


def get_regions_list() -> List[Dict[str, str]]:
    regions = _parse_regions(REGIONS_URL)
    return regions


def get_locations_list(regions: List[Dict[str, str]]) -> List[Dict[str, str]]:
    cities = list()
    for region in regions:
        items = []
        logging.info(f'Parsing region: {region.get("name")}')
        url = region.get('url')
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        content_blocks = soup.find_all('div', class_='col-12 col-lg-4')
        for block in content_blocks:
            rows = block.find_all('tr')
            for row in rows:
                name = row.find('a')
                if name is not None:
                    name = row.find('a').text
                    location_type = row.find(class_='wn').text
                    districts = []
                    # if location_type == 'г.':
                    #     districts = _parse_districts(name)
                    items.append(
                        {
                            'region': region.get('name'),
                            'type': location_type,
                            'name': name,
                            'districts': districts,
                            'url': row.find('a')['href'],
                            'lat': None,
                            'lon': None
                        }
                    )
        cities.extend(items)
    return cities


def _parse_regions(url: str, region: str = None) -> List[Dict[str, str]]:
    items = list()
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content_blocks = soup.find_all('div', class_='col-12 col-lg-4')
    for block in content_blocks:
        links = block.find_all('a')
        for link in links:
            url = link['href']
            region_name = link.text
            item = {
                'name': region_name,
                'url': f'{REGIONS_URL}{url}',
            }
            items.append(item)
    return items


def _get_districts(url: str) -> List[str]:
    districts = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            thumbcaption = soup.find(class_='thumbcaption')
            spans = thumbcaption.find_all('span')
            if len(spans) != 0:
                for s in spans:
                    text = s.text
                    if text != '' and text != '\xa0\xa0\xa0\xa0':
                        districts.append(s.text)
            links = thumbcaption.find_all('a')
            if len(links) != 0:
                for l in links:
                    text = l.text
                    if text != '':
                        districts.append(l.text)
    except:
        ...
    return districts


def _parse_districts(city_name: str) -> List[str]:
    url = f'https://ru.wikipedia.org/wiki/{city_name}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.find('div', id='bodyContent')
        districts_url = ''
        links = content.find_all('a')
        for link in links:
            if match(f'^Административное деление (?:\w*\b)?{city_name[:-2]}.*', link.text, IGNORECASE) is not None or \
                    match(f'^Административно-территориальное деление (?:\w*\b)?{city_name[:-2]}.*', link.text, IGNORECASE) is not None:
                districts_url = f'https://ru.wikipedia.org/{link["href"]}'
        if districts_url != '':
            return _get_districts(districts_url)
    return []


if __name__ == '__main__':
    ...
    # regions_ = get_regions_list()
    # locations = get_locations_list(regions_)
    #
    # with open('locations_with_urls.json', 'w') as file:
    #     json.dump(locations, file, ensure_ascii=False)
    #
    # #

    with open('locations.json') as f:
        locations = json.load(f)

    for location in locations:
        location_url = location.get('url')
        url = f'{REGIONS_URL}{location_url}'
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='table table-striped')
        tds = table.find_all('td')
        coordinates = tds[-1]

        pattern = r'\d+\.\d+'
        matches = re.findall(pattern, coordinates.text)

        lat = float(matches[0])
        lon = float(matches[1])
        location['lat'] = lat
        location['lon'] = lon

    # with open('locations_with_urls.json') as f:
    #     locations_with_urls = json.load(f)
    #
    # locations = sorted(locations, key=lambda x: x.get('name'))
    # locations_with_urls = sorted(locations_with_urls, key=lambda x: x.get('name'))
    #
    # # print(len(locations), len(locations_with_urls))
    #
    # for i in range(len(locations)):
    #     locations[i]['url'] = locations_with_urls[i].get('url')
    #
    # # for location in locations:
    # #     print(location)
    #
    with open('locations.json', 'w') as file:
        json.dump(locations, file, ensure_ascii=False)



