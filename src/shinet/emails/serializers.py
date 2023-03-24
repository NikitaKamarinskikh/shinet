from rest_framework import serializers


class IsEmailAvailableSerializers(serializers.Serializer):
    email = serializers.EmailField()
