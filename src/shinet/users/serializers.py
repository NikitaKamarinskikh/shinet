from rest_framework import serializers

from . import models


class AddNotificationTokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class SwapNotificationStatusSerializer(serializers.Serializer):
    notification_status = serializers.BooleanField()


class UserSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserSettings
        fields = '__all__'

