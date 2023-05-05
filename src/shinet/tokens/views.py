from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .jwt import JWT
from .serializers import UpdateAccessTokenSerializer
from .exceptions import InvalidAccessTokenException
from shinet.services import HTTP_422_RESPONSE_SWAGGER_SCHEME, make_422_response


class UpdateAccessTokenAPIView(GenericAPIView):
    serializer_class = UpdateAccessTokenSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Token updated successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            status.HTTP_403_FORBIDDEN: 'Forbidden',
            status.HTTP_422_UNPROCESSABLE_ENTITY: HTTP_422_RESPONSE_SWAGGER_SCHEME
        }
    )
    def patch(self, request):
        data = request.data
        serializer = UpdateAccessTokenSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        access_token = data.get('access_token')
        refresh_token = data.get('refresh_token')
        try:
            access_jwt = JWT(access_token)
            refresh_jwt = JWT(refresh_token)
            if refresh_jwt.is_available():
                jwt = JWT(access_jwt.payload, update_time=True)
                return Response(status=status.HTTP_200_OK, data={
                    'access_token': jwt.access_token
                })
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except InvalidAccessTokenException:
            return Response(status=status.HTTP_403_FORBIDDEN)




