from django.db.utils import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from tokens.jwt import JWT
from tokens.services import create_refresh_token
from .serializers import MasterCreationSerializer
from users.settings import UsersRoles
from .registration_services import save_phone_numbers


class MastersRegistrationAPIView(GenericAPIView):
    serializer_class = MasterCreationSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Client created',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
            status.HTTP_409_CONFLICT: 'Email conflict'
        }
    )
    def post(self, request):
        data = request.data
        data['role'] = UsersRoles.MASTER.value
        master_serializer = MasterCreationSerializer(data=data)
        if master_serializer.is_valid():
            try:
                master = master_serializer.save()
                if request.data.get('phone_numbers_lit') is not None:
                    save_phone_numbers(master.pk, request.data.get('phone_numbers_lit'))
                master.master_info.specializations.add(
                    *request.data.get('specializations_ids_list')
                )
                jwt_payload = {
                    'user_id': master.pk
                }
                jwt = JWT(jwt_payload)
                response_data = {
                    'access_token': jwt.access_token,
                    'refresh_token': jwt.refresh_token
                }
                create_refresh_token(user_id=master.id, token=response_data.get('refresh_token'))
                return Response(status=status.HTTP_201_CREATED, data=response_data)
            except IntegrityError:
                return Response(status=status.HTTP_409_CONFLICT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
