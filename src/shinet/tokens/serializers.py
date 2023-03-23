from rest_framework import serializers


class UpdateRefreshTokenSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
