from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from tokens.decorators import check_access_token


class TermsOfUseAPIView(GenericAPIView):

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: 'Data',
        }
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
