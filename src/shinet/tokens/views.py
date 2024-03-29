from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .jwt import JWT
from .serializers import UpdateAccessTokenSerializer
from users.services import get_user_by_id_or_none


class UpdateAccessTokenAPIView(GenericAPIView):
    serializer_class = UpdateAccessTokenSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Update access token',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            status.HTTP_403_FORBIDDEN: 'Forbidden',
        }
    )
    def patch(self, request):
        serializer = UpdateAccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data.get('refresh_token')
        try:
            refresh_jwt = JWT(refresh_token)
            if refresh_jwt.is_available():
                payload = refresh_jwt.payload
                user_id = payload.get('user_id')
                user = get_user_by_id_or_none(user_id)
                if user is None:
                    return Response(status=status.HTTP_403_FORBIDDEN)
                new_payload = {
                    'user_id': user.pk,
                }
                if user.master_info:
                    new_payload['master_id'] = user.master_info.pk
                jwt = JWT(new_payload, update_time=True)
                return Response(status=status.HTTP_200_OK, data={
                    'access_token': jwt.access_token
                })
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(status=status.HTTP_403_FORBIDDEN)

