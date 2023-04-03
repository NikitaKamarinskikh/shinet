from rest_framework import serializers
from users.models import Users
from  users.common.serializers import UserRegistrationSerializer
from users.common.services import make_sha256_hash


class MasterCreationSerializer(UserRegistrationSerializer):
    specializations_ids_list = serializers.ListField(
        child=serializers.IntegerField(), min_length=1)
    phone_numbers_lit = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    location = serializers.CharField(max_length=255)

    def create(self, validated_data):
        validated_data['password'] = make_sha256_hash(validated_data['password'])
        del validated_data['specializations_ids_list']
        if validated_data.get('phone_numbers_lit') is not None:
            del validated_data['phone_numbers_lit']
        del validated_data['location']
        return Users.objects.create(**validated_data)

