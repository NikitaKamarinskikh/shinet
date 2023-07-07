"""
This module contains serializers for verification and verification codes
"""
from rest_framework import serializers


class SendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={
        'invalid': 'Некорректный адрес',
    })


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={
        'invalid': 'Некорректный адрес',
    })
    code = serializers.IntegerField()


class VerificationTokenSerializer(serializers.Serializer):
    verification_token = serializers.CharField()



