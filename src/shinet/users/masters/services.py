"""
This module contains some functions for masters
"""
from __future__ import annotations
from typing import Optional

from subscriptions.services import get_active_master_subscription_or_none
from users.models import MasterInfo, Users
from users.services import get_user_phone_numbers


def get_master_info_by_id_or_none(master_id: int) -> MasterInfo | None:
    """

    """
    return MasterInfo.objects.filter(pk=master_id).first()


def get_master_by_id_or_none(user_id: int) -> Optional[Users]:
    """

    """
    user = Users.objects.select_related('master_info').filter(pk=user_id).first()
    if user is None:
        return None
    master_phone_numbers = get_user_phone_numbers(user.pk)
    subscription = get_active_master_subscription_or_none(user.master_info.pk)
    setattr(user, 'phone_numbers', master_phone_numbers)
    setattr(user, 'master_subscription', subscription)
    return user



