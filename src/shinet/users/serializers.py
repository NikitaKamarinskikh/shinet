from rest_framework import serializers

from . import models


class AddNotificationTokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class SwapNotificationStatusSerializer(serializers.Serializer):
    notification_status = serializers.BooleanField()


class UserSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserSettings
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Users
        fields = '__all__'


class BaseUserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    settings = UserSettingsSerializer()

    class Meta:
        model = models.Users
        exclude = ('password', 'master_info',
                   'role')


class EditUserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EditUserPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()



