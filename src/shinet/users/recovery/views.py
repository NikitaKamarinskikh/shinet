"""
This module contains APIView class for recover account
"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from users.registration.services import make_sha256_hash
from users.models import Users
from .serializers import RecoverPasswordSerializer


class RecoverPasswordAPIView(GenericAPIView):
    serializer_class = RecoverPasswordSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: 'Password changed',
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'Invalid parameters',
        },
    )
    def patch(self, request):
        data = request.data.copy()
        client_serializer = RecoverPasswordSerializer(data=data)
        if client_serializer.is_valid():
            password = request.data.get('password')
            email = request.data.get('email')
            client = Users.objects.get(email=email)
            password = make_sha256_hash(password)
            client.password = password
            client.save()
            return Response(status=status.HTTP_200_OK)
        return Response(client_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



