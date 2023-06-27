"""
This module contains additional functions for `slots` app
"""
from __future__ import annotations
from typing import List
from datetime import datetime
from .models import Slots, Bookings

MINIMAL_SLOT_TIME_IN_MINUTES = 30
MAXIMAL_SLOT_TIME_IN_HOURS = 16
AVAILABLE_MINUTES = ('00', '15', '30')


def get_slots_with_bookings_by_date_range_and_master_id(master_id: int,
                                          start_date: datetime,
                                          end_date: datetime) -> List[Slots]:
    """

    """
    return list(Slots.objects.prefetch_related('bookings').filter(
        master_id=master_id,
        start_datetime__date__gte=start_date,
        end_datetime__date__lte=end_date
    ))


def get_slots_by_date_range_and_master_id(master_id: int,
                                          start_date: datetime = None,
                                          end_date: datetime = None) -> List[Slots]:
    """

    """
    filters = {
        'master_id': master_id,
    }
    if start_date is not None:
        filters['start_datetime__date__gte'] = start_date
    if end_date is not None:
        filters['end_datetime__date__lte'] = end_date
    return list(Slots.objects.filter(**filters))


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


def get_bookings_by_slot_id(slot_id: int) -> List[Bookings]:
    """

    """
    return list(Bookings.objects.filter(slot_id=slot_id))


def save_booking(slot_id: int, service_id: int, client_id: int,
                 start_datetime: datetime, end_datetime: datetime) -> Bookings:
    """

    """
    return Bookings.objects.create(
        slot_id=slot_id,
        service_id=service_id,
        client_id=client_id,
        start_datetime=start_datetime,
        end_datetime=end_datetime
    )


def get_booking_by_id_or_none(booking_id: int) -> Bookings | None:
    return Bookings.objects.select_related('service', 'client').filter(pk=booking_id).first()



