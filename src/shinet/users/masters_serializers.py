from rest_framework.serializers import ModelSerializer, ListField, IntegerField
from .models import Users
from .common_services import make_sha256_hash


class MasterCreationSerializer(ModelSerializer):
    specializations_ids_list = ListField(child=IntegerField())

    def create(self, validated_data):
        validated_data['password'] = make_sha256_hash(validated_data['password'])
        del validated_data['specializations_ids_list']
        return super().create(validated_data)

    class Meta:
        model = Users
        fields = ('email', 'password', 'first_name',
                  'last_name', 'sex', 'specializations_ids_list')

