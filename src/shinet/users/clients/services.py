"""

"""
from typing import Optional

from users.models import Users, UsersPhonesNumbers


def get_client_by_id_or_none(client_id: int) -> Optional[Users]:
    """

    """
    return Users.objects.filter(pk=client_id).first()


def update_client(client_id: int, data: dict) -> int:
    """

    """
    return Users.objects.filter(pk=client_id).update(**data)


def get_client_phone_number_by_user_id_or_none(user_id: int) -> Optional[str]:
    """

    """
    return UsersPhonesNumbers.objects.values_list('phone_number', flat=True).\
        filter(user_id=user_id).first()


def get_client_by_filters_or_none(client_id: int, **filters) -> Optional[Users]:
    """

    """
    return Users.objects.filter(pk=client_id, **filters).first()


def create_or_replace_client_phone_number(user_id: int, phone_number: str) -> UsersPhonesNumbers:
    """

    """
    phone_number_instance = UsersPhonesNumbers.objects.filter(user_id=user_id).first()
    if phone_number_instance is None:
        phone_number_instance = UsersPhonesNumbers.objects.create(user_id=user_id, phone_number=phone_number)
    else:
        phone_number_instance.phone_number = phone_number
        phone_number_instance.save()
    return phone_number_instance






