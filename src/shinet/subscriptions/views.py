from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from . import serializers
from .models import Subscriptions
from .services import get_master_subscriptions


class SubscriptionListAPIView(ListAPIView):
    queryset = Subscriptions.objects.all()
    serializer_class = serializers.SubscriptionSerializer

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
            status.HTTP_200_OK: serializers.SubscriptionSerializer(many=True),
            status.HTTP_403_FORBIDDEN: 'Access denied'
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SubscriptionsHistoryAPIView(ListAPIView):
    serializer_class = serializers.MastersSubscriptionSerializer

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
            status.HTTP_200_OK: serializers.MastersSubscriptionSerializer(many=True),
            status.HTTP_403_FORBIDDEN: 'Access denied'
        },
        query_serializer=serializers.MastersSubscriptionHistoryQuerySerializer()
    )
    def get(self, request, *args, **kwargs):
        serializer = serializers.MastersSubscriptionHistoryQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        master_id = serializer.validated_data.get('master_id')
        self.queryset = get_master_subscriptions(master_id)
        return super().get(request, *args, **kwargs)


class SubscriptionsPaymentAPIView(GenericAPIView):

    def post(self, request):
        ...




