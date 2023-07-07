from rest_framework import serializers

from users.models import Users


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = '__all__'


class BaseClientSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()

    class Meta:
        model = Users
        exclude = ('password', 'settings', 'master_info',
                   'role')


class EditClientSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)


class EditClientEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EditClientPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()



