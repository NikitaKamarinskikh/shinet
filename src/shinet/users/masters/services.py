"""
This module contains some functions for masters
"""
from __future__ import annotations
from users.models import MasterInfo


def get_master_info_by_id_or_none(master_id: int) -> MasterInfo | None:
    """

    """
    return MasterInfo.objects.filter(pk=master_id).first()

