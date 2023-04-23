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
        fields = '__all__'


class MastersSubscriptionHistoryQuerySerializer(serializers.Serializer):
    master_id = serializers.IntegerField()


class SubscriptionsPaymentSerializer(serializers.Serializer):
    master_id = serializers.IntegerField()
    subscription_id = serializers.IntegerField()

