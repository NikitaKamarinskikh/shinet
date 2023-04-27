import logging

from django.http import HttpRequest
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from shinet.services import HTTP_422_RESPONSE_SWAGGER_SCHEME
from tokens.decorators import check_access_token
from .models import Specializations
from tokens.services import get_payload_from_token
from tokens.exceptions import InvalidAccessTokenException
from . import serializers
from .services import get_master_services, save_master_service,\
    get_service_by_id_and_master_id_or_none, update_master_service


class SpecializationsAPIView(ListAPIView):
    serializer_class = serializers.SpecializationsSerializer
    queryset = Specializations.objects.all()


class MastersServicesListAPIView(GenericAPIView):
    serializer_class = serializers.MasterServiceSerializer

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
            status.HTTP_200_OK: serializers.MasterServiceSerializer(many=True),
            status.HTTP_403_FORBIDDEN: 'Access denied'
        },
    )
    @check_access_token
    def get(self, request: HttpRequest):
        try:
            payload = get_payload_from_token(request)
            master_id = payload.get('master_id')
            if master_id is None:
                return Response(status=status.HTTP_403_FORBIDDEN)
            services = get_master_services(master_id)
            serializer = serializers.MasterServiceSerializer(services, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except InvalidAccessTokenException:
            return Response(status=status.HTTP_403_FORBIDDEN)


class AddMasterServiceAPIView(GenericAPIView):
    serializer_class = serializers.AddMasterServiceSerializer

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
            status.HTTP_200_OK: 'Ok',
            status.HTTP_422_UNPROCESSABLE_ENTITY: HTTP_422_RESPONSE_SWAGGER_SCHEME,
            status.HTTP_403_FORBIDDEN: 'Access denied'
        },
    )
    @check_access_token
    def post(self, request: HttpRequest):
        try:
            payload = get_payload_from_token(request)
            master_id = payload.get('master_id')
            if master_id is None:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = serializers.AddMasterServiceSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            save_master_service(master_id, serializer)
            return Response(status=status.HTTP_200_OK)
        except InvalidAccessTokenException:
            return Response(status=status.HTTP_403_FORBIDDEN)


class EditMasterServiceAPIView(GenericAPIView):
    serializer_class = serializers.EditMasterServiceSerializer

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
            status.HTTP_200_OK: 'Ok',
            status.HTTP_422_UNPROCESSABLE_ENTITY: HTTP_422_RESPONSE_SWAGGER_SCHEME,
            status.HTTP_403_FORBIDDEN: 'Access denied'
        },
    )
    @check_access_token
    def patch(self, request):
        try:
            payload = get_payload_from_token(request)
            master_id = payload.get('master_id')
            if master_id is None:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = serializers.AddMasterServiceSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = request.data
            service_id = data.get('service_id')
            del data['service_id']
            update_master_service(master_id, service_id, data)
            return Response(status=status.HTTP_200_OK)
        except InvalidAccessTokenException:
            return Response(status=status.HTTP_403_FORBIDDEN)


class DeleteMasterServiceAPIView(GenericAPIView):
    serializer_class = serializers.EditMasterServiceSerializer

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
            status.HTTP_200_OK: 'Ok',
            status.HTTP_403_FORBIDDEN: 'Access denied',
            status.HTTP_404_NOT_FOUND: 'Service not found'
        },
    )
    @check_access_token
    def delete(self, request, service_id: int):
        try:
            payload = get_payload_from_token(request)
            master_id = payload.get('master_id')
            if master_id is None:
                return Response(status=status.HTTP_403_FORBIDDEN)
            service = get_service_by_id_and_master_id_or_none(service_id, master_id)
            if service is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            service.delete()
            return Response(status=status.HTTP_200_OK)
        except InvalidAccessTokenException:
            return Response(status=status.HTTP_403_FORBIDDEN)

