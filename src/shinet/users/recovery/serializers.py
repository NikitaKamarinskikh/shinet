from rest_framework import serializers


class RecoverPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
