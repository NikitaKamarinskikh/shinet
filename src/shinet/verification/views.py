"""
This module contains APIView class for masters and clients registration
"""
import logging
from smtplib import SMTPRecipientsRefused
from datetime import datetime, timezone

from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from shinet.services import HTTP_422_RESPONSE_SWAGGER_SCHEME, make_422_response
from .models import VerificationCodes
from . import services
from . import serializers


class SendVerificationCodeAPIView(GenericAPIView):
    serializer_class = serializers.SendVerificationCodeSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: 'Code sent successfully',
            status.HTTP_422_UNPROCESSABLE_ENTITY: HTTP_422_RESPONSE_SWAGGER_SCHEME
        }
    )
    def post(self, request):
        serializer = serializers.SendVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')

        user = services.get_user_by_email_or_none(email)
        if user is not None:
            return make_422_response({'email': 'Email already in use'})

        code = services.create_unique_code()

        try:
            services.send_verification_code(email, code)
        except SMTPRecipientsRefused:
            return make_422_response({'email': 'Cannot send email to this address'})
        except Exception as e:
            logging.exception(e)
            return make_422_response({'email': 'Cannot send email to this address'})

        services.create_or_replace_verification_code(email, code)
        return Response(status=status.HTTP_200_OK)


class VerifyCodeAPIView(GenericAPIView):
    serializer_class = serializers.VerifyCodeSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: serializers.VerificationTokenSerializer(),
            status.HTTP_422_UNPROCESSABLE_ENTITY: HTTP_422_RESPONSE_SWAGGER_SCHEME
        }
    )
    def post(self, request):
        serializer = serializers.VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        code = serializer.validated_data.get('code')
        verification_code = services.get_verification_code_by_code_and_email_or_none(email, code)
        if verification_code is not None:
            if verification_code.expiration_time >= datetime.now(timezone.utc):
                verification_code.delete()
                verification_token_data = {
                    'email': email,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
                }
                verification_token = services.generate_verification_token(verification_token_data)
                response_serializer = serializers.VerificationTokenSerializer(data={
                    'verification_token': verification_token
                })
                return Response(status=status.HTTP_200_OK, data=response_serializer.data)
            verification_code.delete()
            return make_422_response({'email': 'Verification code expired'})
        return make_422_response({'code': 'Invalid verification code'})



