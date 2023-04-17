from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
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
            status.HTTP_422_UNPROCESSABLE_ENTITY: openapi.Response(
                description="Validation error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "errors": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "field": openapi.Schema(type="string"),
                                    "message": openapi.Schema(type="string"),
                                },
                            ),
                        ),
                    },
                ),
            )
        }
    )
    def post(self, request):
        data = request.data
        auth_serializer = UserAuthenticationSerializer(data=data)
        if auth_serializer.is_valid():
            try:
                user = auth_serializer.get_user()
                if user.status == UsersStatuses.BLOCKED.value:
                    return Response(status=status.HTTP_403_FORBIDDEN)
                refresh_token = get_refresh_token_or_none(user.pk)
                if refresh_token is not None:
                    return Response(status=status.HTTP_304_NOT_MODIFIED)
                jwt = JWT({
                    'user_id': user.pk
                })
                create_refresh_token(user_id=user.id, token=jwt.refresh_token)
                return Response(status=status.HTTP_200_OK, data=jwt.as_dict())
            except Users.DoesNotExist:
                return Response({
                        'password': 'Invalid password'
                    }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response(auth_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

