from rest_framework import serializers


class UpdateAccessTokenSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    refresh_token = serializers.CharField()
