from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .serializers import LocationsQuerySerializer, LocationsListSerializer
from .services import load_locations


class LocationsAPIView(GenericAPIView):

    @swagger_auto_schema(
        query_serializer=LocationsQuerySerializer(),
        responses={
            status.HTTP_200_OK: LocationsListSerializer(many=True)
        },
        operation_description='Location types: `city`, `village (село, аул и т.п)`, `countryside (деревня)`'
    )
    def get(self, request):
        serializer = LocationsQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        page = serializer.validated_data.get('page')
        quantity = serializer.validated_data.get('quantity')
        pattern = serializer.validated_data.get('pattern')

        locations = load_locations()
        if pattern is not None:
            filtered_locations = []
            for city in locations:
                if pattern.lower() in city.name.lower():
                    filtered_locations.append(city)
        else:
            filtered_locations = locations.copy()

        start_position = page * quantity
        filtered_locations = filtered_locations[start_position:start_position + quantity]

        filtered_locations = [item.json for item in filtered_locations]
        serializer = LocationsListSerializer(data=filtered_locations, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

