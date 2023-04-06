from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from datetime import datetime, timezone
from tokens.jwt import JWT
from tokens.services import create_refresh_token, get_refresh_token_or_none
from users.models import Users, VerificationCodes
from users.settings import UsersStatuses
from .serializers import UserAuthenticationSerializer, IsEmailAvailableSerializers, SendVerificationCodeSerializer,\
    VerifyCodeSerializer, UpdateVerificationCodeSerializer
from .services import send_verification_code, save_verification_code, \
    get_verification_code_by_code_and_email_or_none, update_verification_code_by_email, \
    create_unique_code, get_user_by_email_or_none


class UserAuthenticationAPIView(GenericAPIView):
    serializer_class = UserAuthenticationSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='User authenticated',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            status.HTTP_304_NOT_MODIFIED: 'Already authorized',
            status.HTTP_403_FORBIDDEN: 'Forbidden (If user is blocked)',
            status.HTTP_422_UNPROCESSABLE_ENTITY: openapi.Response(
                description='Validation error',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'email': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Validation error message'
                        ),
                        'password': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Validation error message'
                        ),
                    }
                )
            )
        }
    )
    def post(self, request):
        data = request.data
        auth_serializer = UserAuthenticationSerializer(data=data)
        if auth_serializer.is_valid():
            try:
                user = auth_serializer.get_user()
                if user.status == UsersStatuses.BLOCKED.value:
                    return Response(status=status.HTTP_403_FORBIDDEN)
                refresh_token = get_refresh_token_or_none(user.pk)
                if refresh_token is not None:
                    return Response(status=status.HTTP_304_NOT_MODIFIED)
                jwt = JWT({
                    'user_id': user.pk
                })
                create_refresh_token(user_id=user.id, token=jwt.refresh_token)
                return Response(status=status.HTTP_200_OK, data=jwt.as_dict())
            except Users.DoesNotExist:
                return Response({
                        'password': 'Invalid password'
                    }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response(auth_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class SendVerificationCodeAPIView(GenericAPIView):
    serializer_class = SendVerificationCodeSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: 'Code sent successfully',
            status.HTTP_422_UNPROCESSABLE_ENTITY: openapi.Response(
                description='Validation error',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'email': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Validation error message'
                        ),
                    }
                )
            )
        }
    )
    def post(self, request):
        data = request.data
        serializer = IsEmailAvailableSerializers(data=data)
        if serializer.is_valid():
            email = request.data.get('email')
            user = get_user_by_email_or_none(email)
            if user is not None:
                return Response({
                    'email': 'Email already in use'
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            code = create_unique_code()
            save_verification_code(email, code)
            send_verification_code(email, code)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class VerifyCodeAPIView(GenericAPIView):
    serializer_class = VerifyCodeSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: 'Coded verified',
            status.HTTP_422_UNPROCESSABLE_ENTITY: openapi.Response(
                description='Validation error',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'email': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Validation error message'
                        ),
                        'code': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Validation error message'
                        ),
                    }
                )
            )
        }
    )
    def post(self, request):
        data = request.data
        serializer = VerifyCodeSerializer(data=data)
        if serializer.is_valid():
            email = request.data.get('email')
            code = request.data.get('code')
            verification_code = get_verification_code_by_code_and_email_or_none(email, code)
            if verification_code is not None:
                if verification_code.expiration_time >= datetime.now(timezone.utc):
                    verification_code.delete()
                    return Response(status=status.HTTP_200_OK)
                verification_code.delete()
                return Response({
                    'email': 'Verification code expired'
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                return Response({
                    'code': 'Invalid verification code'
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class UpdateVerificationCodeAPIView(GenericAPIView):
    serializer_class = UpdateVerificationCodeSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: 'Coded sent successfully',
            status.HTTP_422_UNPROCESSABLE_ENTITY: openapi.Response(
                description='Validation error',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'email': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Validation error message'
                        ),
                    }
                )
            )
        }
    )
    def post(self, request):
        data = request.data
        serializer = UpdateVerificationCodeSerializer(data=data)
        if serializer.is_valid():
            email = request.data.get('email')
            code = create_unique_code()
            try:
                send_verification_code(email, code)
                update_verification_code_by_email(email, code)
                return Response(status=status.HTTP_200_OK)
            except VerificationCodes.DoesNotExist:
                return Response({
                    'code': 'Verification code does not exists'
                }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
