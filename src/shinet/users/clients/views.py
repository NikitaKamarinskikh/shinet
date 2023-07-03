import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from tokens.decorators import check_access_token
from tokens.jwt import JWT
from tokens.services import get_payload_from_token
from . import serializers
from . import services
from ..services import get_user_phone_numbers


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
    def get(self, request):
        payload = get_payload_from_token(request)
        user_id = payload.get('user_id')
        if user_id is None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        client = services.get_client_by_id_or_none(user_id)
        if client is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        client_phone_numbers = get_user_phone_numbers(client.pk)
        setattr(client, 'phone_numbers', client_phone_numbers)
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
    def patch(self, request):

        payload = get_payload_from_token(request)
        user_id = payload.get('user_id')
        if user_id is None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        client = services.get_client_by_id_or_none(user_id)
        if client is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.EditClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print(serializer.validated_data)
        if 'email' in serializer.validated_data:
            print('email', 'email', 'email')

        services.update_client(user_id, serializer.validated_data)

        # updated_client = services.get_client_by_id_or_none(user_id)

        # response_serializer = serializers.ClientSerializer(updated_client)
        response_serializer = serializers.ClientSerializer(client)
        return Response(status=status.HTTP_200_OK, data=response_serializer.data)


