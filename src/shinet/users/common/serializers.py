from rest_framework import serializers
from users.models import Users
from users.common.services import make_sha256_hash


class UserRegistrationSerializer(serializers.Serializer):
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


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={
        'invalid': 'Invalid email address.',
    })


class UserAuthenticationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def get_user(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        password = make_sha256_hash(password)
        return Users.objects.get(email=email, password=password)


class IsEmailAvailableSerializers(EmailSerializer):
    ...

class SendVerificationCodeSerializer(EmailSerializer):
   ...


class VerifyCodeSerializer(EmailSerializer):
    code = serializers.IntegerField()


class UpdateVerificationCodeSerializer(EmailSerializer):
    ...

