from .models import VerificationCodes
from .services import send_verification_code, save_verification_code,\
    get_verification_code_by_code_and_email_or_none, update_verification_code_by_email,\
    create_unique_code
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from users.common.services import get_user_by_email_or_none
from .serializers import IsEmailAvailableSerializers, SendCodeSerializer,\
    VerifyCodeSerializer, UpdateodeSerializer


class IsEmailAvailableAPIView(GenericAPIView):
    serializer_class = IsEmailAvailableSerializers

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: 'Email available',
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_409_CONFLICT: 'Email not available'
        }
    )
    def post(self, request):
        data = request.data
        serializer = IsEmailAvailableSerializers(data=data)
        if serializer.is_valid():
            email = request.data.get('email')
            user = get_user_by_email_or_none(email)
            if user is None:
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SendCodeAPIView(GenericAPIView):
    serializer_class = SendCodeSerializer

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
            code = create_unique_code()
            email = request.data.get('email')
            save_verification_code(email, code)
            send_verification_code(email, code)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeAPIView(GenericAPIView):
    serializer_class = VerifyCodeSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: 'Coded verified',
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
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
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateCodeAPIView(GenericAPIView):
    serializer_class = UpdateodeSerializer

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

