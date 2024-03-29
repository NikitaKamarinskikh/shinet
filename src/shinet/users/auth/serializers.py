from rest_framework import serializers
from users.models import Users
from users.registration.services import make_sha256_hash


class UserAuthenticationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def get_user(self) -> Users:
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        password = make_sha256_hash(password)
        return Users.objects.get(email=email, password=password)

