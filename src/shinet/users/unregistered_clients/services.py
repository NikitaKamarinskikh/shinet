"""
This module contains some additional functions for `unregistered_clients`package
"""
from __future__ import annotations
from typing import List, Optional

from users.models import UnregisteredClients, MasterInfo


def save_unregistered_client(master_id: int, first_name: str,
                             last_name: str, extra_info: str = None) -> UnregisteredClients:
    """

    """
    return UnregisteredClients.objects.create(
        master_id=master_id,
        first_name=first_name,
        last_name=last_name,
        extra_info=extra_info
    )


def get_unregistered_clients_by_master_id(master_id: int) -> List[UnregisteredClients]:
    """

    """
    return UnregisteredClients.objects.filter(master_id=master_id)


def get_unregistered_client_by_id_or_none(unregistered_client_id: int) -> Optional[UnregisteredClients]:
    """

    """
    return UnregisteredClients.objects.filter(pk=unregistered_client_id).first()



