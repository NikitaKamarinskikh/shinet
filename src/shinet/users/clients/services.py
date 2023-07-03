"""

"""
from typing import Optional

from users.models import Users


def get_client_by_id_or_none(client_id: int) -> Optional[Users]:
    """

    """
    return Users.objects.filter(pk=client_id).first()


def update_client(client_id: int, data: dict) -> int:
    """

    """
    return Users.objects.filter(pk=client_id).update(**data)


