"""
This module contains APIView class for masters and clients registration
"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from datetime import datetime, timezone
from shinet.services import HTTP_422_RESPONSE_SWAGGER_SCHEME, make_422_response
from users.models import VerificationCodes
from users.verification.serializers import IsEmailAvailableSerializers, SendVerificationCodeSerializer,\
    VerifyCodeSerializer, UpdateVerificationCodeSerializer
from . import services as verification_services


class SendVerificationCodeAPIView(GenericAPIView):
    serializer_class = SendVerificationCodeSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: 'Code sent successfully',
            status.HTTP_422_UNPROCESSABLE_ENTITY: HTTP_422_RESPONSE_SWAGGER_SCHEME
        }
    )
    def post(self, request):
        data = request.data
        serializer = IsEmailAvailableSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        user = verification_services.get_user_by_email_or_none(email)
        if user is not None:
            return make_422_response({'email': 'Email already in use'})
        code = verification_services.create_unique_code()
        verification_services.save_verification_code(email, code)
        verification_services.send_verification_code(email, code)
        return Response(status=status.HTTP_200_OK)


class VerifyCodeAPIView(GenericAPIView):
    serializer_class = VerifyCodeSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: 'Coded verified',
            status.HTTP_422_UNPROCESSABLE_ENTITY: HTTP_422_RESPONSE_SWAGGER_SCHEME
        }
    )
    def post(self, request):
        data = request.data
        serializer = VerifyCodeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        code = request.data.get('code')
        verification_code = verification_services.get_verification_code_by_code_and_email_or_none(email, code)
        if verification_code is not None:
            if verification_code.expiration_time >= datetime.now(timezone.utc):
                verification_code.delete()
                return Response(status=status.HTTP_200_OK)
            verification_code.delete()
            return make_422_response({'email': 'Verification code expired'})
        return make_422_response({'code': 'Invalid verification code'})


class UpdateVerificationCodeAPIView(GenericAPIView):
    serializer_class = UpdateVerificationCodeSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: 'Coded sent successfully',
            status.HTTP_422_UNPROCESSABLE_ENTITY: HTTP_422_RESPONSE_SWAGGER_SCHEME
        }
    )
    def patch(self, request):
        data = request.data
        serializer = UpdateVerificationCodeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        code = verification_services.create_unique_code()
        try:
            verification_services.update_verification_code_by_email(email, code)
            verification_services.send_verification_code(email, code)
            return Response(status=status.HTTP_200_OK)
        except VerificationCodes.DoesNotExist:
            return make_422_response({'code': 'Verification code does not exists'})
