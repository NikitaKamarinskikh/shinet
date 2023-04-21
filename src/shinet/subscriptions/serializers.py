"""
This module contains serializers for `subscriptions` app
"""
from rest_framework import serializers
from .models import Subscriptions


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = '__all__'




