from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .jwt import JWT
from .serializers import UpdateAccessTokenSerializer


class UpdateAccessTokenAPIView(GenericAPIView):
    serializer_class = UpdateAccessTokenSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Token updated successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
        }
    )
    def post(self, request):
        data = request.data
        serializer = UpdateAccessTokenSerializer(data=data)
        if serializer.is_valid():
            user_id = int(data.get('user_id'))
            refresh_token = data.get('refresh_token')
            refresh_jwt = JWT(refresh_token)
            if refresh_jwt.is_available():
                jwt = JWT({'user_id': user_id})
                return Response(status=status.HTTP_200_OK, data={
                    'access_token': jwt.access_token
                })
        return Response(status=status.HTTP_400_BAD_REQUEST)


