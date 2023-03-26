"""
This module contains functions with logic
for masters registration
"""
from string import digits
from random import choice
from typing import Tuple
from users.models import UsersPhonesNumbers, MasterInfo


def save_phone_numbers(user_id: int, phone_numbers: Tuple[str]) -> None:
    """Saves the phone numbers to db
    :param user_id: user id in database
    :type user_id: int
    :param phone_numbers: user phone numbers
    :type phone_numbers: Tuple[str]
    :return: Nothing
    :rtype: None
    """
    phones_object = [
        UsersPhonesNumbers(user_id=user_id, phone_number=phone_number)
        for phone_number in phone_numbers
    ]
    UsersPhonesNumbers.objects.bulk_create(phones_object)


def create_uuid() -> int:
    """ Create 6-digit unique identifier for master
    :return: 6-digit unique identifier
    :rtype: int
    """
    current_identifiers = MasterInfo.objects.values_list('uuid', flat=True)

    while True:
        uuid = ''.join(choice(digits) for _ in range(6))
        if uuid not in current_identifiers:
            return int(uuid)


