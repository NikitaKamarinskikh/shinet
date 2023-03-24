from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class TermsOfUseAPIView(GenericAPIView):

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: 'Data',
        }
    )
    def get(self, request):
        data = {
            'text': 'Input terms of use here'
        }
        return Response(
            status=status.HTTP_200_OK,
            data=data
        )
