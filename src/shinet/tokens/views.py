from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .services import create_or_update_refresh_token
from .jwt import JWT
from .serializers import UpdateRefreshTokenSerializer


class UpdateRefreshTokenAPIView(GenericAPIView):
    serializer_class = UpdateRefreshTokenSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Token updated successfully',
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
        serializer = UpdateRefreshTokenSerializer(data=data)
        if serializer.is_valid():
            user_id = int(data.get('user_id'))
            jwt = JWT({'user_id': user_id})
            create_or_update_refresh_token(user_id, jwt.refresh_token)
            return Response(status=status.HTTP_200_OK, data=jwt.as_dict())
        return Response(status=status.HTTP_400_BAD_REQUEST)


