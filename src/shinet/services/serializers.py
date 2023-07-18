from drf_yasg import openapi
from rest_framework import serializers
from .models import Specializations, Services


class SpecializationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Specializations
        fields = '__all__'


class MasterServiceSerializer(serializers.ModelSerializer):
    specialization = SpecializationsSerializer()

    class Meta:
        model = Services
        fields = ('id', 'specialization', 'name', 'price',
                  'duration_in_minutes', 'description', 'image')


class CreateMasterServiceSerializer(serializers.Serializer):
    specialization_id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.IntegerField(min_value=0)
    duration_in_minutes = serializers.IntegerField()
    description = serializers.CharField()
    image = serializers.ImageField(required=False)


class EditMasterServiceSerializer(serializers.Serializer):
    service_id = serializers.IntegerField()
    specialization_id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    price = serializers.IntegerField(min_value=0, required=False)
    duration_in_minutes = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False)


class MasterServicesListQuerySerializer(serializers.Serializer):
    limit = serializers.IntegerField(required=False)

