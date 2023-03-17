from rest_framework import serializers
from .models import Users
from .common_services import make_sha256_hash


class MasterCreationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    sex = serializers.CharField()
    role = serializers.CharField(required=False)
    specializations_ids_list = serializers.ListField(
        child=serializers.IntegerField(), min_length=1)

    def create(self, validated_data):
        validated_data['password'] = make_sha256_hash(validated_data['password'])
        del validated_data['specializations_ids_list']
        return Users.objects.create(**validated_data)

