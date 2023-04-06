"""VerificationCodes:
This module contains serializers for verification and verification codes
"""
from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={
        'invalid': 'Некорректный адрес',
    })


class IsEmailAvailableSerializers(EmailSerializer):
    ...


class SendVerificationCodeSerializer(EmailSerializer):
    ...


class VerifyCodeSerializer(EmailSerializer):
    code = serializers.IntegerField()


class UpdateVerificationCodeSerializer(EmailSerializer):
    ...

