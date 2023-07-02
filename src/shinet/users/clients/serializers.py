from rest_framework import serializers

from users.models import Users


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = '__all__'


class BaseClientSerializer(serializers.ModelSerializer):
    phone_numbers = serializers.ListField(
        child=serializers.CharField(), required=False
    )

    class Meta:
        model = Users
        exclude = ('password', 'settings', 'master_info',
                   'role', 'created_at')



