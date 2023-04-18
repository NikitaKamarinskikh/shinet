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
    regions = _parse_content(REGIONS_URL)
    return regions


def get_cities_list(regions: List[Dict[str, str]]) -> List[Dict[str, str]]:
    cities = list()
    for region in regions:
        logging.info(f'Parsing region: {region.get("name")}')
        url = region.get('url')
        items = _parse_content(url, region.get('name'))
        cities.extend(items)
    return cities


def _parse_content(url: str, region: str = None) -> List[Dict[str, str]]:
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
    # regions_ = get_regions_list()
    # cities_ = get_cities_list(regions_)
    # with open('cities.json', 'w') as file:
    #     json.dump(cities_, file, ensure_ascii=False)
    with open('cities.json') as f:
        data = json.load(f)
    c = []
    for item in data:
        c.append(item.get('name'))
    print(len(c))
