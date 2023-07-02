"""

"""
import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from tokens.decorators import check_access_token
from tokens.jwt import JWT
from . import serializers
from . import services


class UnregisteredClientsListAPIView(ListAPIView):
    serializer_class = serializers.UnregisteredClientSerializer

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
            status.HTTP_200_OK: serializers.UnregisteredClientSerializer(many=True),
            status.HTTP_403_FORBIDDEN: 'Access denied'
        },
    )
    @check_access_token
    def get(self, request, *args, **kwargs):
        try:
            auth_token = request.META.get('HTTP_AUTHORIZATION')
            _, access_token = auth_token.split()
            jwt = JWT(access_token)
            master_id = jwt.payload.get('master_id')
            if master_id is None:
                return Response(status=status.HTTP_403_FORBIDDEN)
            clients = services.get_unregistered_clients_by_master_id(master_id)
            serializer = serializers.UnregisteredClientSerializer(clients, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as e:
            logging.error(e)
            return Response(status=status.HTTP_403_FORBIDDEN)


class CreateUnregisteredClientAPIView(GenericAPIView):
    serializer_class = serializers.UnregisteredClientSerializer

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
            status.HTTP_200_OK: 'Client created',
            status.HTTP_403_FORBIDDEN: 'Access denied'
        },
    )
    @check_access_token
    def post(self, request):
        try:
            auth_token = request.META.get('HTTP_AUTHORIZATION')
            _, access_token = auth_token.split()
            jwt = JWT(access_token)
            master_id = jwt.payload.get('master_id')
            if master_id is None:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logging.error(e)
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.UnregisteredClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        first_name = serializer.validated_data.get('first_name')
        last_name = serializer.validated_data.get('last_name')
        extra_info = serializer.validated_data.get('extra_info')

        services.save_unregistered_client(master_id, first_name, last_name, extra_info)

        return Response(status=status.HTTP_200_OK)

