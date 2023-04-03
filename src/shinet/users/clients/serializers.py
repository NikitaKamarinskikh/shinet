from rest_framework import serializers
from users.models import Users
from users.common.services import make_sha256_hash
from users.common.serializers import UserRegistrationSerializer


class ClientCreationSerializer(UserRegistrationSerializer):
    ...


