from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tokens.decorators import check_access_token


class TermsOfUseAPIView(APIView):

    @swagger_auto_schema(
        request_headers={
            'Authorization': 'Bearer <token>'
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                'Access token',
                type=openapi.TYPE_STRING),
        ],
    )
    @check_access_token
    def get(self, request):
        data = {
            'text': 'Input terms of use here'
        }
        return Response(
            status=status.HTTP_200_OK,
            data=data
        )
