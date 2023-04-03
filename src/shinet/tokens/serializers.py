from rest_framework import serializers


class UpdateAccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(error_messages={
        'required': 'Access token required'
    })
    refresh_token = serializers.CharField(error_messages={
        'required': 'Refresh token required'
    })
