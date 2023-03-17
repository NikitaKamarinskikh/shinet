from rest_framework import serializers
from .models import Users
from .common_services import make_sha256_hash


class ClientCreationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    sex = serializers.CharField()
    role = serializers.CharField(required=False)

    def create(self, validated_data):
        return Users.objects.create(**validated_data)
