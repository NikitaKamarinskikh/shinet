from rest_framework import serializers
from users.models import Users
from users.locations.serializers import LocationSerializer
from .services import make_sha256_hash


class ClientRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    sex = serializers.CharField()
    role = serializers.CharField(required=False)
    profile_image = serializers.ImageField(required=False)

    def create(self, validated_data):
        validated_data['password'] = make_sha256_hash(validated_data['password'])
        return Users.objects.create(**validated_data)


class MasterRegistrationSerializer(ClientRegistrationSerializer):
    specializations_ids_list = serializers.ListField(
        child=serializers.IntegerField(), min_length=1)
    phone_numbers_lit = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    location = LocationSerializer()

    def create(self, validated_data):
        validated_data['password'] = make_sha256_hash(validated_data['password'])
        del validated_data['specializations_ids_list']
        if validated_data.get('phone_numbers_lit') is not None:
            del validated_data['phone_numbers_lit']
        del validated_data['location']
        return Users.objects.create(**validated_data)

