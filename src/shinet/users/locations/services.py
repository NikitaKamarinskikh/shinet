"""
This module contains some additional functions for locations
"""
import json
from typing import NamedTuple, List
from dataclasses import dataclass


@dataclass
class Location:
    name: str
    districts: List[str]

    @property
    def json(self):
        return {
            'name': self.name,
            'districts': self.districts
        }


def load_locations() -> List[Location]:
    locations = list()
    with open('users/locations/cities.json') as f:
        data = json.load(f)
        for location in data:
            locations.append(
                Location(
                    name=location.get('name'),
                    districts=[]
                )
            )
    return locations





