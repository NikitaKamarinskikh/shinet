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
from .registration_services import save_phone_numbers, create_uuid


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
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'Invalid arguments',
        },
        operation_description='You can also add `profile_image` parameter with client photo profile'
    )
    def post(self, request):
        data = request.data
        data['role'] = UsersRoles.MASTER.value
        master_serializer = MasterCreationSerializer(data=data)
        if master_serializer.is_valid():
            master = master_serializer.save()
            location = request.data.get('location')
            uuid = create_uuid()
            master.master_info.location = location
            master.master_info.uuid = uuid
            master.master_info.save()
            if request.data.get('phone_numbers_lit') is not None:
                save_phone_numbers(master.pk, request.data.get('phone_numbers_lit'))
            try:
                master.master_info.specializations.add(
                    *request.data.get('specializations_ids_list')
                )
            except IntegrityError:
                ...
            jwt = JWT({
                'user_id': master.pk
            })
            create_refresh_token(user_id=master.pk, token=jwt.refresh_token)
            return Response(status=status.HTTP_201_CREATED, data=jwt.as_dict())
        else:
            return Response(master_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        serializer.fields.pop('role', None)
        return serializer
