"""
This module contains APIView class for masters and clients registration
"""
import logging

from django.db.utils import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from subscriptions.services import save_master_trial_subscription
from tokens.jwt import JWT
from tokens.services import create_refresh_token
from verification.decorators import check_verification_token
from .serializers import MasterRegistrationSerializer, ClientRegistrationSerializer
from shinet.services import HTTP_422_RESPONSE_SWAGGER_SCHEME, make_422_response
from users.settings import UsersRoles
from .services import save_phone_numbers, create_uuid
from ..locations.serializers import LocationSerializer
from ..models import UserSettings, MasterInfo, Locations
from verification.services import get_user_by_email_or_none


class ClientsRegistrationAPIView(GenericAPIView):
    serializer_class = ClientRegistrationSerializer

    @swagger_auto_schema(
        request_headers={
            'Verification': 'Bearer <token>'
        },
        manual_parameters=[
            openapi.Parameter(
                'Verification', openapi.IN_HEADER, 'Verification token',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Client created',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            status.HTTP_422_UNPROCESSABLE_ENTITY: HTTP_422_RESPONSE_SWAGGER_SCHEME
        },
        operation_description='You can also add `profile_image` parameter with client photo profile'
    )
    @check_verification_token
    def post(self, request):
        data = request.data.copy()
        data['role'] = UsersRoles.CLIENT.value
        client_serializer = ClientRegistrationSerializer(data=data)
        client_serializer.is_valid(raise_exception=True)
        try:
            client = client_serializer.save()
            settings = UserSettings.objects.create()
            client.settings = settings
            client.save()
            jwt = JWT({
                'user_id': client.pk
            })
            create_refresh_token(user_id=client.id, token=jwt.refresh_token)
            return Response(status=status.HTTP_200_OK, data=jwt.as_dict())
        except IntegrityError:
            return make_422_response({'email': 'Email already in use'})

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        serializer.fields.pop('role', None)
        return serializer


class MastersRegistrationAPIView(GenericAPIView):
    serializer_class = MasterRegistrationSerializer

    @swagger_auto_schema(
        request_headers={
            'Verification': 'Bearer <token>'
        },
        manual_parameters=[
            openapi.Parameter(
                'Verification', openapi.IN_HEADER, 'Verification token',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Client created',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            status.HTTP_422_UNPROCESSABLE_ENTITY: HTTP_422_RESPONSE_SWAGGER_SCHEME
        },
        operation_description='You can also add `profile_image` parameter with client photo profile'
    )
    @check_verification_token
    def post(self, request):
        data = request.data
        data['role'] = UsersRoles.MASTER.value

        master_serializer = MasterRegistrationSerializer(data=data)
        location_serializer = LocationSerializer(data=request.data.get('location'))

        master_serializer.is_valid(raise_exception=True)
        location_serializer.is_valid(raise_exception=True)

        email = request.data.get('email')
        if get_user_by_email_or_none(email) is not None:
            return make_422_response({'email': 'Email already in use'})
        master = master_serializer.save()
        master_info = MasterInfo.objects.create()
        settings = UserSettings.objects.create()
        master.master_info = master_info
        master.settings = settings
        master.save()

        location = location_serializer.save()
        uuid = create_uuid()
        master.master_info.location = location
        master.master_info.uuid = uuid
        master.master_info.save()

        save_master_trial_subscription(master.master_info.pk)
        if request.data.get('phone_numbers_lit') is not None:
            save_phone_numbers(master.pk, request.data.get('phone_numbers_lit'))
        try:
            master.master_info.specializations.add(
                *request.data.get('specializations_ids_list')
            )
        except Exception as e:
            logging.error(e)
        jwt = JWT({
            'user_id': master.pk,
            'master_id': master.master_info.pk
        })
        create_refresh_token(user_id=master.pk, token=jwt.refresh_token)
        return Response(status=status.HTTP_200_OK, data=jwt.as_dict())

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        serializer.fields.pop('role', None)
        return serializer
