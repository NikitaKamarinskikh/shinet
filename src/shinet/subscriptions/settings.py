"""
This module contains some additional settings for subscription package
"""

from enum import Enum


class SubscriptionTypes(Enum):
    """This class contains all subscription types"""
    TRIAL = 'trial'

    @classmethod
    def choices(cls) -> tuple:
        return tuple((item.name, item.value) for item in cls)

