from rest_framework.serializers import ModelSerializer
from .models import Users
from .common_services import make_sha256_hash


class ClientCreationSerializer(ModelSerializer):

    def create(self, validated_data):
        validated_data['password'] = make_sha256_hash(validated_data['password'])
        return super().create(validated_data)

    class Meta:
        model = Users
        fields = ('email', 'password', 'first_name',
                  'last_name', 'sex')

