from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from tokens.jwt import JWT
from tokens.services import create_refresh_token
from users.models import Users
from .serializers import UserAuthenticationSerializer


class UserAuthenticationAPIView(GenericAPIView):
    serializer_class = UserAuthenticationSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='User authenticated',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            status.HTTP_400_BAD_REQUEST: 'Bad request',
            status.HTTP_404_NOT_FOUND: 'User not found',
        }
    )
    def post(self, request):
        data = request.data
        auth_serializer = UserAuthenticationSerializer(data=data)
        if auth_serializer.is_valid():
            try:
                user = auth_serializer.get_user()
                jwt_payload = {
                    'user_id': user.pk
                }
                jwt = JWT(jwt_payload)
                response_data = {
                    'access_token': jwt.access_token,
                    'refresh_token': jwt.refresh_token
                }
                create_refresh_token(user_id=user.id, token=response_data.get('refresh_token'))
                return Response(status=status.HTTP_200_OK, data=response_data)
            except Users.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)
