"""
This module contains functions for parsing Russian cities
"""
from __future__ import annotations
import logging
import requests
import json
from bs4 import BeautifulSoup
from typing import List, Tuple, Dict
from re import match


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
                    items.append(
                        {
                            'region': region.get('name'),
                            'type': location_type,
                            'name': name,
                            'districts': [],
                            'url': row.find('a')['href']
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
            if region is not None:
                item['region'] = region
            items.append(item)
    return items


if __name__ == '__main__':
    regions_ = get_regions_list()
    locations = get_locations_list(regions_)
    with open('locations.json', 'w') as file:
        json.dump(locations, file, ensure_ascii=False)
    # with open('cities.json') as f:
    #     data = json.load(f)
    # c = []
    # for item in data:
    #     c.append(item.get('name'))
    # print(len(c))


