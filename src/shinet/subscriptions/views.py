from datetime import datetime, timedelta, timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from shinet.services import HTTP_422_RESPONSE_SWAGGER_SCHEME, make_422_response
from users.masters.services import get_master_info_by_id_or_none
from . import serializers
from .models import Subscriptions, MastersSubscriptions
from . import services


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
        self.queryset = services.get_master_subscriptions(master_id)
        return super().get(request, *args, **kwargs)


class SubscriptionsPaymentAPIView(GenericAPIView):
    serializer_class = serializers.SubscriptionsPaymentSerializer

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
            status.HTTP_200_OK: serializers.MastersSubscriptionSerializer(),
            status.HTTP_403_FORBIDDEN: 'Access denied'
        },
    )
    def post(self, request):
        serializer = serializers.SubscriptionsPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        master_id = serializer.validated_data.get('master_id')
        subscription_id = serializer.validated_data.get('subscription_id')

        subscription = services.get_subscription_by_id_or_none(subscription_id)
        if subscription is None:
            return make_422_response({'subscription_id': 'Subscription does not exists'})
        if subscription.type == Subscriptions.Types.TRIAL.value:
            return make_422_response({'subscription_id': 'Subscription cannot be trial'})

        master_info = get_master_info_by_id_or_none(master_id)
        if master_info is None:
            return make_422_response({'master_id': 'Master does not exists'})

        paid_subscriptions = services.get_paid_master_subscriptions(master_id)

        if len(paid_subscriptions) > 0:
            last_subscription = paid_subscriptions[0]
            start_date = last_subscription.end_date + timedelta(days=1)
            end_date = services.get_subscription_end_time(start_date, 30)
            master_subscription = services.save_master_subscription(
                master_id=master_id,
                subscription_id=subscription_id,
                start_date=start_date,
                end_date=end_date,
                status=MastersSubscriptions.Status.PAID.value,
                paying_price=subscription.price_with_discount
            )
            serializer = serializers.MastersSubscriptionSerializer(master_subscription)
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        # If have active subscription
        current_active_subscription = services.get_active_master_subscription_or_none(master_id)
        if current_active_subscription is not None:
            start_date = current_active_subscription.end_date + timedelta(days=1)
            end_date = services.get_subscription_end_time(start_date, 30)
            master_subscription = services.save_master_subscription(
                master_id=master_id,
                subscription_id=subscription_id,
                start_date=start_date,
                end_date=end_date,
                status=MastersSubscriptions.Status.PAID.value,
                paying_price=subscription.price_with_discount
            )
            serializer = serializers.MastersSubscriptionSerializer(master_subscription)
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        # Has no subscriptions
        start_date = datetime.utcnow().date()
        end_date = services.get_subscription_end_time(start_date, 30)
        master_subscription = services.save_master_subscription(
            master_id=master_id,
            subscription_id=subscription_id,
            start_date=start_date,
            end_date=end_date,
            status=MastersSubscriptions.Status.PAID.value,
            paying_price=subscription.price_with_discount
        )
        serializer = serializers.MastersSubscriptionSerializer(master_subscription)
        return Response(status=status.HTTP_200_OK, data=serializer.data)



