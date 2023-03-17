from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .clients_serializers import ClientCreationSerializer
from .settings import UsersRoles
from tokens.jwt import JWT


class ClientsRegistrationAPIView(GenericAPIView):
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
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
        }
    )
    def post(self, request):
        data = request.data
        data['role'] = UsersRoles.CLIENT.value
        client_serializer = ClientCreationSerializer(data=request.data)
        if client_serializer.is_valid():
            client = client_serializer.save()
            jwt_payload = {
                'user_id': client.pk
            }
            jwt = JWT(jwt_payload)
            response_data = {
                'access_token': jwt.access_token,
                'refresh_token': jwt.refresh_token
            }
            return Response(status=status.HTTP_201_CREATED, data=response_data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

