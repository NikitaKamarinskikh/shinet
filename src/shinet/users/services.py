from typing import List

from . import models


def get_user_phone_numbers(user_id: int) -> List[str]:
    """

    """
    return list(models.UsersPhonesNumbers.objects.values_list('phone_number', flat=True).filter(user_id=user_id))




