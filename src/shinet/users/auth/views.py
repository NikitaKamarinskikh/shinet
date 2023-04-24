from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from shinet.services import HTTP_422_RESPONSE_SWAGGER_SCHEME, make_422_response
from tokens.jwt import JWT
from tokens.services import create_refresh_token, get_refresh_token_or_none
from users.models import Users
from users.settings import UsersStatuses
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
            status.HTTP_304_NOT_MODIFIED: 'Already authorized',
            status.HTTP_403_FORBIDDEN: 'Forbidden (If user is blocked)',
            status.HTTP_422_UNPROCESSABLE_ENTITY: HTTP_422_RESPONSE_SWAGGER_SCHEME
        }
    )
    def post(self, request):
        data = request.data
        auth_serializer = UserAuthenticationSerializer(data=data)
        auth_serializer.is_valid(raise_exception=True)
        try:
            user = auth_serializer.get_user()
            if user.status == UsersStatuses.BLOCKED.value:
                return Response(status=status.HTTP_403_FORBIDDEN)
            refresh_token = get_refresh_token_or_none(user.pk)
            if refresh_token is not None:
                return Response(status=status.HTTP_304_NOT_MODIFIED)
            jwt_payload = {
                'user_id': user.pk
            }
            if user.master_info:
                jwt_payload['master_id'] = user.master_info.pk
            jwt = JWT(jwt_payload)
            create_refresh_token(user_id=user.pk, token=jwt.refresh_token)
            return Response(status=status.HTTP_200_OK, data=jwt.as_dict())
        except Users.DoesNotExist:
            return make_422_response({'password': 'Invalid password'})


