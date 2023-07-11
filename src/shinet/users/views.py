import logging

from django.db.utils import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView


from shinet.services import HTTP_422_RESPONSE_SWAGGER_SCHEME, make_422_response
from tokens.decorators import check_access_token
from tokens.services import get_payload_from_access_token
from . import services
from . import serializers


class AddNotificationTokenAPIView(GenericAPIView):
    serializer_class = serializers.AddNotificationTokenSerializer

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
            status.HTTP_200_OK: '',
            status.HTTP_403_FORBIDDEN: 'Access denied',
            status.HTTP_422_UNPROCESSABLE_ENTITY: HTTP_422_RESPONSE_SWAGGER_SCHEME
        },
    )
    @check_access_token
    def post(self, request):
        payload = get_payload_from_access_token(request)
        user_id = payload.get('user_id')
        if user_id is None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.AddNotificationTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data.get('token')
        services.create_notification_token_if_not_exists(user_id, token)
        return Response(status=status.HTTP_200_OK)


class SwapUserNotificationStatusAPIView(GenericAPIView):

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
            status.HTTP_200_OK: serializers.SwapNotificationStatusSerializer,
            status.HTTP_403_FORBIDDEN: 'Access denied',
            status.HTTP_422_UNPROCESSABLE_ENTITY: HTTP_422_RESPONSE_SWAGGER_SCHEME
        },
    )
    def patch(self, request):
        payload = get_payload_from_access_token(request)
        user_id = payload.get('user_id')
        if user_id is None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            notification_status = services.swap_user_notification_status(user_id)
            response_serializer = serializers.SwapNotificationStatusSerializer(
                {
                    'notification_status': notification_status
                }
            )
            return Response(status=status.HTTP_200_OK, data=response_serializer.data)
        except Exception as e:
            logging.exception(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


