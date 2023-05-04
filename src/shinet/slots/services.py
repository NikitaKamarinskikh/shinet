"""
This module contains additional functions for `slots` app
"""
from __future__ import annotations
from typing import List
from datetime import datetime
from .models import Slots


MINIMAL_SLOT_TIME_IN_MINUTES = 30
MAXIMAL_SLOT_TIME_IN_HOURS = 16
AVAILABLE_MINUTES = ('00', '15', '30')


def get_slots_by_date_range_and_master_id(master_id: int,
                                          start_date: datetime,
                                          end_date: datetime) -> List[Slots]:
    """

    """
    return list(Slots.objects.filter(
        master_id=master_id,
        start_datetime__date__gte=start_date,
        end_datetime__date__lte=end_date
    ))


def get_slots_by_master_id(master_id: int) -> List[Slots]:
    """

    """
    return list(Slots.objects.filter(master_id=master_id))


def create_slot(master_id: int, start_datetime: datetime, end_datetime: datetime) -> Slots:
    """

    """
    return Slots.objects.create(
        master_id=master_id,
        start_datetime=start_datetime,
        end_datetime=end_datetime
    )




