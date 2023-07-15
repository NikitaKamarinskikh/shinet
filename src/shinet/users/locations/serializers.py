from rest_framework import serializers
from users.models import Locations


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = '__all__'


class LocationsQuerySerializer(serializers.Serializer):
    pattern = serializers.CharField(required=False)
    page = serializers.IntegerField(required=False, default=0, min_value=0, max_value=100_000)
    quantity = serializers.IntegerField(required=False, default=10, min_value=0, max_value=100_000)


class LocationsListSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.CharField()
    region = serializers.CharField()
    districts = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True,
        min_length=0
    )
