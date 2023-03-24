from rest_framework import serializers


class IsEmailAvailableSerializers(serializers.Serializer):
    email = serializers.EmailField()


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField()


class UpdateodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
