from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from users.common.services import get_user_by_email_or_none
from .serializers import IsEmailAvailableSerializers


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
