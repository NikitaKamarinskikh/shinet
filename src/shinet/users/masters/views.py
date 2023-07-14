import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from shinet.services import make_422_response
from users.registration.services import make_sha256_hash
from subscriptions.services import get_active_master_subscription_or_none
from users.models import UsersPhonesNumbers
from tokens.decorators import check_access_token
from services.services import get_specializations_by_ids_list
from tokens.jwt import JWT
from tokens.services import get_payload_from_access_token
from verification.decorators import check_verification_token
from . import serializers
from . import services
from users.services import get_user_phone_numbers
from ..models import Locations


class MasterDetailAPIView(GenericAPIView):

    @swagger_auto_schema(
        request_headers={
            'Authorization': 'Bearer <token>'
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, 'Access token',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            status.HTTP_200_OK: serializers.MasterSerializer(),
            status.HTTP_404_NOT_FOUND: 'Master not found',
            status.HTTP_403_FORBIDDEN: 'Access denied',
        },
        operation_description='',
    )
    @check_access_token
    def get(self, request):
        payload = get_payload_from_access_token(request)
        user_id = payload.get('user_id')
        master_id = payload.get('master_id')
        if user_id is None or master_id is None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        master = services.get_master_by_id_or_none(user_id)
        if master is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        master = services.get_master_by_id_or_none(user_id)
        response_serializer = serializers.MasterSerializer(master)
        return Response(status=status.HTTP_200_OK, data=response_serializer.data)


class EditMasterAPIView(GenericAPIView):
    serializer_class = serializers.EditMasterSerializer

    @swagger_auto_schema(
        request_headers={
            'Authorization': 'Bearer <token>'
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, 'Access token',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            status.HTTP_200_OK: serializers.MasterSerializer(),
            status.HTTP_404_NOT_FOUND: 'Master not found',
            status.HTTP_403_FORBIDDEN: 'Access denied',
        },
        operation_description='',
    )
    @check_access_token
    def patch(self, request):
        payload = get_payload_from_access_token(request)
        user_id = payload.get('user_id')
        master_id = payload.get('master_id')
        if user_id is None or master_id is None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.EditMasterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        master = services.get_master_by_id_or_none(user_id)

        if serializer.validated_data.get('first_name'):
            master.first_name = serializer.validated_data.get('first_name')
        if serializer.validated_data.get('last_name'):
            master.first_name = serializer.validated_data.get('last_name')
        if serializer.validated_data.get('specializations'):
            specializations = get_specializations_by_ids_list(serializer.validated_data.get('specializations'))
            master.master_info.specializations.set(specializations)
        if serializer.validated_data.get('location'):
            Locations.objects.filter(pk=master.master_info.location.pk).update(
                **(serializer.validated_data.get('location'))
            )
            location = Locations.objects.get(pk=master.master_info.location.pk)
            master.master_info.location = location
        if serializer.validated_data.get('phone_numbers'):
            UsersPhonesNumbers.objects.filter(pk=user_id).delete()
            new_phone_numbers = [
                UsersPhonesNumbers(user_id=user_id, phone_number=phone_number)
                for phone_number in serializer.validated_data.get('phone_numbers')
            ]
            UsersPhonesNumbers.objects.bulk_create(new_phone_numbers)
        if serializer.validated_data.get('description'):
            master.master_info.description = serializer.validated_data.get('description')

        master.save()

        updated_master = services.get_master_by_id_or_none(user_id)
        response_serializer = serializers.MasterSerializer(updated_master)
        return Response(status=status.HTTP_200_OK, data=response_serializer.data)



