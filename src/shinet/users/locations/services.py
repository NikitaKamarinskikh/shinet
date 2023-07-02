"""
This module contains some additional functions for locations
"""
import json
from typing import NamedTuple, List
from dataclasses import dataclass


@dataclass
class Location:
    name: str
    type: str
    region: str
    districts: List[str]

    @property
    def json(self):
        return {
            'name': self.name,
            'type': self.type,
            'region': self.region,
            'districts': self.districts
        }


def load_locations() -> List[Location]:
    locations = list()
    with open('users/locations/locations.json') as f:
        data = json.load(f)
        for location in data:
            locations.append(
                Location(
                    name=location.get('name'),
                    type=location.get('type'),
                    region=location.get('region'),
                    districts=location.get('districts')
                )
            )
    return locations

