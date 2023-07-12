"""
This module contains some functions for masters
"""
from __future__ import annotations
from typing import Optional

from users.models import MasterInfo, Users


def get_master_info_by_id_or_none(master_id: int) -> MasterInfo | None:
    """

    """
    return MasterInfo.objects.filter(pk=master_id).first()


def get_master_by_id_or_none(user_id: int) -> Optional[Users]:
    """

    """
    return Users.objects.filter(pk=user_id).first()


