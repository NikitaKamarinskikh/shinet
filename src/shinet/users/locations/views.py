from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from tokens.jwt import JWT
from tokens.services import create_refresh_token, get_refresh_token_or_none
from users.models import Users
from users.settings import UsersStatuses


class LocationsAPIView(GenericAPIView):

    @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter(
                    'offset',
                    openapi.IN_QUERY,
                    description="Offset",
                    type=openapi.TYPE_STRING
                ),
                openapi.Parameter(
                    'cities_number',
                    openapi.IN_QUERY,
                    description="Number of cities",
                    type=openapi.TYPE_INTEGER
                )
            ],
            operation_description="Get a list of users"
    )
    def get(self, request):
        ...



# class MyAPIView(APIView):
#     serializer_class = MySerializer
#
#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter(
#                 'name',
#                 openapi.IN_QUERY,
#                 description="Name of the user to filter by",
#                 type=openapi.TYPE_STRING
#             ),
#             openapi.Parameter(
#                 'age',
#                 openapi.IN_QUERY,
#                 description="Age of the user to filter by",
#                 type=openapi.TYPE_INTEGER
#             )
#         ],
#         operation_description="Get a list of users"
#     )
#     def get(self, request, *args, **kwargs):
#         name = request.query_params.get('name')
#         age = request.query_params.get('age')
#         queryset = User.objects.all()
#         if name:
#             queryset = queryset.filter(name=name)
#         if age:
#             queryset = queryset.filter(age=age)
#         serializer = MySerializer(queryset, many=True)
#         return Response(serializer.data)

