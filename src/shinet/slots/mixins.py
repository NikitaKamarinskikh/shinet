from typing import Dict, List
from datetime import datetime, timedelta

from .services import MINIMAL_SLOT_TIME_IN_MINUTES, MAXIMAL_SLOT_TIME_IN_HOURS
from .date_range import DateRange, InvalidDateRangeException


class ValidationResult:

    def __init__(self, errors: Dict[str, str] = None, is_valid: bool = False):
        self._is_valid = is_valid
        self._errors = errors

    @property
    def errors(self):
        return self._errors

    def is_valid(self) -> bool:
        return self._is_valid


class SlotsValidationMixin:

    def validate_slot_dates(self, master_id: int, start_datetime: datetime, end_datetime: datetime, slots):
        now = datetime.now()
        try:
            date_range = DateRange(start_datetime, end_datetime)
        except InvalidDateRangeException:
            return ValidationResult({'start_datetime': 'Start date must be earlier than end date'})
        if start_datetime == end_datetime:
            return ValidationResult({'end_datetime': 'End date must not be same as start_date'})
        if date_range.duration_in_minutes < MINIMAL_SLOT_TIME_IN_MINUTES:
            return ValidationResult({'end_datetime': f'Minimal slot time is {MINIMAL_SLOT_TIME_IN_MINUTES} minutes'})
        if date_range.duration_in_hours > MAXIMAL_SLOT_TIME_IN_HOURS:
            return ValidationResult({'end_datetime': f'Maximal slot time is {MAXIMAL_SLOT_TIME_IN_HOURS} hours'})
        if start_datetime < now:
            return ValidationResult({'start_datetime': 'Start date is too old'})
        if end_datetime < now:
            return ValidationResult({'end_datetime': 'End date is too old'})

        time_validation = self._validate_slot_time(date_range)
        if not time_validation.is_valid():
            return time_validation

        intersection_result = self._check_intersection_with_clients_slots(master_id, date_range, slots)
        if not intersection_result.is_valid():
            return intersection_result

        unregistered_intersection_result = self._check_intersections_with_unregistered_clients_slots(master_id, date_range)
        if not unregistered_intersection_result.is_valid():
            return unregistered_intersection_result

        return ValidationResult(is_valid=True)

    def _validate_slot_time(self, date_range: DateRange) -> ValidationResult:
        start_time_minutes_str = str(date_range.start_time).split(':')[1]
        end_time_minutes_str = str(date_range.end_time).split(':')[1]
        if int(start_time_minutes_str) % 5 != 0:
            return ValidationResult({'start_datetime': 'Invalid start date minutes'})
        if int(end_time_minutes_str) % 5 != 0:
            return ValidationResult({'end_datetime': 'Invalid end date minutes'})
        return ValidationResult(is_valid=True)

    def _check_intersection_with_clients_slots(self, master_id: int, date_range: DateRange, slots) -> ValidationResult:
        for slot in slots:
            slot_date_range = DateRange(slot.start_datetime, slot.end_datetime)
            if date_range.has_intersection(slot_date_range, include_start=False, include_end=False) or\
                    date_range.is_equal(slot_date_range) or \
                    (slot_date_range.includes(date_range.end_datetime) and slot_date_range.start_datetime == date_range.start_datetime) or \
                    (slot_date_range.includes(date_range.start_datetime) and slot_date_range.end_datetime == date_range.end_datetime):
                return ValidationResult({'start_date': 'Date range intersection'})
        return ValidationResult(is_valid=True)

    def _check_intersections_with_unregistered_clients_slots(self,  master_id: int, date_range: DateRange) -> ValidationResult:
        return ValidationResult(is_valid=True)


class BookingValidationMixin:

    def validate_booking_time(self, start_datetime: datetime, end_datetime:  datetime,
                              bookings, unregistered_bookings) -> ValidationResult:
        now = datetime.now()
        if start_datetime < now:
            return ValidationResult({'start_datetime': 'Start date is too old'})
        if end_datetime < now:
            return ValidationResult({'end_datetime': 'End date is too old'})
        try:
            new_booking_date_range = DateRange(start_datetime, end_datetime)
        except InvalidDateRangeException:
            return ValidationResult({'end_datetime': 'End date is too old'})

        for booking in bookings:
            booking_range = DateRange(booking.start_datetime, booking.end_datetime)
            if new_booking_date_range.has_intersection(booking_range, include_start=False, include_end=False) or \
                    new_booking_date_range.is_equal(booking_range) or\
                    (booking_range.includes(new_booking_date_range.end_datetime) and booking_range.start_datetime == new_booking_date_range.start_datetime) or \
                    (booking_range.includes(new_booking_date_range.start_datetime) and booking_range.end_datetime == new_booking_date_range.end_datetime):
                return ValidationResult({'start_date': 'Date range intersection'})

        for booking in unregistered_bookings:
            booking_range = DateRange(booking.start_datetime, booking.end_datetime)
            if new_booking_date_range.has_intersection(booking_range, include_start=False, include_end=False) or \
                    new_booking_date_range.is_equal(booking_range) or\
                    (booking_range.includes(new_booking_date_range.end_datetime) and booking_range.start_datetime == new_booking_date_range.start_datetime) or \
                    (booking_range.includes(new_booking_date_range.start_datetime) and booking_range.end_datetime == new_booking_date_range.end_datetime):
                return ValidationResult({'start_date': 'Date range intersection'})

        return ValidationResult(is_valid=True)

