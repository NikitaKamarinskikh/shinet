from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from datetime import datetime, timezone
from tokens.jwt import JWT
from tokens.services import create_refresh_token, get_refresh_token_or_none
from users.models import Users, VerificationCodes
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
            status.HTTP_400_BAD_REQUEST: 'Bad request',
            status.HTTP_404_NOT_FOUND: 'User not found',
        }
    )
    def post(self, request):
        data = request.data
        auth_serializer = UserAuthenticationSerializer(data=data)
        if auth_serializer.is_valid():
            try:
                user = auth_serializer.get_user()
                refresh_token = get_refresh_token_or_none(user.pk)
                if refresh_token is not None:
                    return Response(status=status.HTTP_304_NOT_MODIFIED)
                jwt = JWT({
                    'user_id': user.pk
                })
                create_refresh_token(user_id=user.id, token=jwt.refresh_token)
                return Response(status=status.HTTP_200_OK, data=jwt.as_dict())
            except Users.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(auth_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class SendVerificationCodeAPIView(GenericAPIView):
    serializer_class = SendVerificationCodeSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: 'Coded sent successfully',
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            422: openapi.Response(
                description='Validation error',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'field_name': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='Validation error message'
                                    )
                                )
                            }
                        )
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
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            code = create_unique_code()
            save_verification_code(email, code)
            send_verification_code(email, code)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # if some_condition:
    #         raise ValidationError({'field_name': ['Error message']})

    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         # Do something
    #         return Response({'message': 'Success'})
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    #
    # def get_swagger_schema(self, *args, **kwargs):
    #     schema = super().get_swagger_schema(*args, **kwargs)
    #     schema['responses']['422']['description'] = 'Validation errors'
    #     schema['responses']['422']['schema'] = MySerializer().fields['name'].error_messages
    #     return schema

class VerifyCodeAPIView(GenericAPIView):
    serializer_class = VerifyCodeSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: 'Coded verified',
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_410_GONE: 'Code expired'
        }
    )
    def post(self, request):
        data = request.data
        serializer = IsEmailAvailableSerializers(data=data)
        if serializer.is_valid():
            email = request.data.get('email')
            code = request.data.get('code')
            verification_code = get_verification_code_by_code_and_email_or_none(email, code)
            if verification_code is not None:
                if verification_code.expiration_time >= datetime.now(timezone.utc):
                    verification_code.delete()
                    return Response(status=status.HTTP_200_OK)
                verification_code.delete()
                return Response(status=status.HTTP_410_GONE)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateVerificationCodeAPIView(GenericAPIView):
    serializer_class = UpdateVerificationCodeSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: 'Coded sent successfully',
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
        }
    )
    def post(self, request):
        data = request.data
        serializer = IsEmailAvailableSerializers(data=data)
        if serializer.is_valid():
            email = request.data.get('email')
            code = create_unique_code()
            try:
                update_verification_code_by_email(email, code)
                return Response(status=status.HTTP_200_OK)
            except VerificationCodes.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)
