"""
This module contains serializers for `subscriptions` app
"""
from rest_framework import serializers
from .models import Subscriptions, MastersSubscriptions


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = '__all__'


class MastersSubscriptionSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer()

    class Meta:
        model = MastersSubscriptions
        fields = ('subscription', 'start_date', 'end_date', 'status', 'paying_price')


class MastersSubscriptionHistoryQuerySerializer(serializers.Serializer):
    master_id = serializers.IntegerField()


class SubscriptionsPaymentSerializer(serializers.Serializer):
    subscription_id = serializers.IntegerField()

