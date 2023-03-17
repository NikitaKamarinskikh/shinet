from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .clients_serializers import ClientCreationSerializer


class MastersRegistrationAPIView(GenericAPIView):
    serializer_class = ClientCreationSerializer

    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter('specializations_ids_list', openapi.IN_QUERY,
    #                           description="Ids of chosen specializations", type=openapi.TYPE_ARRAY,
    #                           items=openapi.Items(type=openapi.TYPE_INTEGER),
    #                           required=True),
    #     ]
    # )
    @swagger_auto_schema(
        responses={
            201: openapi.Response(
                description='Client created',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                    required=['id', 'username'],
                ),
            ),
            400: 'Bad Request',
        }
    )
    def post(self, request):
        data = request.data
        data['role'] = 'client'
        client = ClientCreationSerializer(data=request.data)
        if client.is_valid():
            client.save()
        return Response(status=201, data=None)

