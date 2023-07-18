from rest_framework import serializers


class UpdateAccessTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(error_messages={
        'required': 'Refresh token required'
    })
