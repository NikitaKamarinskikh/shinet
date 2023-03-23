"""
This module contains functions with logic
for masters registration
"""
from typing import Tuple
from users.models import UsersPhonesNumbers


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



