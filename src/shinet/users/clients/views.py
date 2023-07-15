import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from shinet.services import make_422_response
from users.registration.services import make_sha256_hash
from tokens.decorators import check_access_token
from tokens.jwt import JWT
from tokens.services import get_payload_from_access_token
from verification.decorators import check_verification_token
from . import serializers
from . import services
from users.clients.services import get_client_phone_number_by_user_id_or_none


class ClientDetailAPIView(GenericAPIView):

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
            status.HTTP_200_OK: serializers.BaseClientSerializer(),
            status.HTTP_404_NOT_FOUND: 'Client not found',
            status.HTTP_403_FORBIDDEN: 'Access denied',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Server error'
        },
        operation_description='This method gets `client_id` from access_token',
    )
    @check_access_token
    def get(self, request):
        payload = get_payload_from_access_token(request)
        user_id = payload.get('user_id')
        if user_id is None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        client = services.get_client_by_id_or_none(user_id)
        if client is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        client_phone_number = get_client_phone_number_by_user_id_or_none(client.pk)
        if client_phone_number is None:
            client_phone_number = ''
        setattr(client, 'phone_number', client_phone_number)
        response_serializer = serializers.BaseClientSerializer(client)
        return Response(status=status.HTTP_200_OK, data=response_serializer.data)


class EditClientAPIView(GenericAPIView):
    serializer_class = serializers.EditClientSerializer

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
            status.HTTP_200_OK: serializers.BaseClientSerializer(),
            status.HTTP_404_NOT_FOUND: 'Client not found',
            status.HTTP_403_FORBIDDEN: 'Access denied',
        },
        operation_description='',
    )
    @check_access_token
    def patch(self, request):
        payload = get_payload_from_access_token(request)
        user_id = payload.get('user_id')
        if user_id is None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        client = services.get_client_by_id_or_none(user_id)
        if client is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.EditClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = dict()
        if serializer.validated_data.get('first_name'):
            data['first_name'] = serializer.validated_data.get('first_name')
        if serializer.validated_data.get('last_name'):
            data['last_name'] = serializer.validated_data.get('last_name')

        services.update_client(user_id, data)

        updated_client = services.get_client_by_id_or_none(user_id)

        phone_number = serializer.validated_data.get('phone_number')
        if phone_number:
            services.create_or_replace_client_phone_number(user_id, phone_number)
            setattr(updated_client, 'phone_number', phone_number)

        response_serializer = serializers.BaseClientSerializer(updated_client)
        return Response(status=status.HTTP_200_OK, data=response_serializer.data)


class DeleteClientAPIView(GenericAPIView):

    @swagger_auto_schema(
        request_headers={
            'Authorization': 'Bearer <token>',
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, 'Access token',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            status.HTTP_200_OK: 'User deleted successfully',
            status.HTTP_404_NOT_FOUND: 'User not found',
            status.HTTP_403_FORBIDDEN: 'Access denied',
        },
        operation_description='This method gets `client_id` from access_token',
    )
    @check_access_token
    def delete(self, request):
        payload = get_payload_from_access_token(request)
        print(payload)
        user_id = payload.get('user_id')
        if user_id is None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        client = services.get_client_by_id_or_none(user_id)
        print(client)
        if client is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        client.delete()
        return Response(status=status.HTTP_200_OK)





