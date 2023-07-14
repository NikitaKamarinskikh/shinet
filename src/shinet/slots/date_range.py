"""
This module contains `DateRange` class
"""
from __future__ import annotations
from datetime import datetime, timedelta, time, date


class InvalidDateRangeException(Exception):

    def __init__(self, message):
        self.message = message


class DateRange:
    """
    This class implements some basic logic for operations with date ranges
    """

    def __init__(self, start_datetime: datetime, end_datetime: datetime, replace_seconds=True, replace_nanoseconds=True):
        if start_datetime > end_datetime:
            raise InvalidDateRangeException('Start date must be earlier than end date')
        if replace_nanoseconds:
            self._start_datetime = start_datetime.replace(microsecond=0)
            self._end_datetime = end_datetime.replace(microsecond=0)
        if replace_seconds:
            self._start_datetime = start_datetime.replace(second=0)
            self._end_datetime = end_datetime.replace(second=0)
        self._start_date = self._start_datetime.date()
        self._end_date = self._end_datetime.date()
        self._start_time = self._start_datetime.time()
        self._end_time = self._end_datetime.time()

    @property
    def start_datetime(self) -> datetime:
        return self._start_datetime

    @property
    def end_datetime(self) -> datetime:
        return self._end_datetime

    @property
    def start_date(self) -> date:
        return self._start_date

    @property
    def end_date(self) -> date:
        return self._end_date

    @property
    def start_time(self) -> time:
        return self._start_time

    @property
    def end_time(self) -> time:
        return self._end_time

    @property
    def duration_in_minutes(self) -> int:
        return (self._end_datetime - self._start_datetime).seconds // 60

    @property
    def duration_in_hours(self) -> int:
        return (self._end_datetime - self._start_datetime).seconds // 3600

    def is_equal(self, other: DateRange) -> bool:
        """

        """
        return self._start_datetime == other._start_datetime and \
            self._end_datetime == other._end_datetime

    def has_intersection(self, other: DateRange, include_start=True, include_end=True) -> bool:
        """

        """
        return self.contains(other, include_start, include_end) or \
            self.contained_id(other, include_start, include_end) or \
            self.includes(other.start_datetime, include_start, include_end) or \
            self.includes(other.end_datetime, include_start, include_end)

    def contains(self, other: DateRange, include_start=True, include_end=True) -> bool:
        """

        """
        if include_start and not include_end:
            return self._start_datetime <= other.start_datetime and self._end_datetime > other.end_datetime
        if not include_start and include_end:
            return self._start_datetime < other.start_datetime and self._end_datetime >= other.end_datetime
        if not include_start and not include_end:
            return self._start_datetime < other.start_datetime and self._end_datetime > other.end_datetime
        return self._start_datetime <= other.start_datetime and self._end_datetime >= other.end_datetime

    def contained_id(self, other: DateRange, include_start=True, include_end=True) -> bool:
        """

        """
        return other.contains(self, include_start, include_end)

    def includes(self, date: datetime, include_start=True, include_end=True) -> bool:
        """

        """
        if include_start and not include_end:
            return self._start_datetime <= date < self._end_datetime
        if not include_start and include_end:
            return self._start_datetime < date <= self._end_datetime
        if not include_start and not include_end:
            return self._start_datetime < date < self._end_datetime
        return self._start_datetime <= date <= self._end_datetime

    def __str__(self) -> str:
        return f'from {self._start_datetime.strftime("%Y.%m.%d %H:%M:%S")} to {self._end_datetime.strftime("%Y.%m.%d %H:%M:%S")}'
