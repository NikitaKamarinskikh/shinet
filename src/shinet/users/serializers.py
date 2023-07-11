from rest_framework import serializers


class AddNotificationTokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class SwapNotificationStatusSerializer(serializers.Serializer):
    notification_status = serializers.BooleanField()


