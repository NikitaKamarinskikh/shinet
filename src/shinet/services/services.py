"""
This module contains some additional functions for `services` package
"""
from __future__ import annotations
from typing import List
from .models import Services, Specializations
from .serializers import AddMasterServiceSerializer


def get_master_services(master_id: int) -> List[Services]:
    """

    """
    return Services.objects.select_related('specialization', 'master').filter(master_id=master_id)


def save_master_service(master_id: int, serializer: AddMasterServiceSerializer) -> Services:
    """

    """
    return Services.objects.create(
        master_id=master_id,
        specialization_id=serializer.validated_data.get('specialization_id'),
        name=serializer.validated_data.get('name'),
        price=serializer.validated_data.get('price'),
        duration_in_minutes=serializer.validated_data.get('duration_in_minutes'),
        description=serializer.validated_data.get('description')
    )


def update_master_service(master_id: int, service_id: int, data: dict) -> Services:
    """

    """
    return Services.objects.filter(master_id=master_id, pk=service_id).update(**data)


def get_service_by_id_and_master_id_or_none(service_id: int, master_id: int) -> Services | None:
    """

    """
    return Services.objects.filter(pk=service_id, master_id=master_id).first()


def get_specializations_by_ids_list(specialization_ids: List[int]) -> List[Specializations]:
    """

    """
    return Specializations.objects.filter(pk__in=specialization_ids)


