"""
This module contains logic of client api views
"""
from django.db.utils import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from .serializers import ClientCreationSerializer
from users.settings import UsersRoles
from tokens.services import create_refresh_token
from tokens.jwt import JWT


class ClientsRegistrationAPIView(CreateAPIView):
    serializer_class = ClientCreationSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Client created',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'Invalid parameters',
        },
        operation_description='You can also add `profile_image` parameter with client photo profile'
    )
    def post(self, request):
        data = request.data.copy()
        data['role'] = UsersRoles.CLIENT.value
        client_serializer = ClientCreationSerializer(data=data)
        if client_serializer.is_valid():
            try:
                client = client_serializer.save()
                jwt = JWT({
                    'user_id': client.pk
                })
                create_refresh_token(user_id=client.id, token=jwt.refresh_token)
                return Response(status=status.HTTP_201_CREATED, data=jwt.as_dict())
            except IntegrityError:
                return Response({
                    'email': 'Email already in use'
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response(client_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        serializer.fields.pop('role', None)
        return serializer
