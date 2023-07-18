from rest_framework import serializers

from users.models import Users, MasterInfo, UserSettings
from users.locations.serializers import LocationSerializer
from users.serializers import UserSettingsSerializer
from subscriptions.serializers import MastersSubscriptionSerializer


class MasterInfoSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = MasterInfo
        fields = '__all__'


class MasterSerializer(serializers.ModelSerializer):
    settings = UserSettingsSerializer()
    master_info = MasterInfoSerializer()
    phone_numbers = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    master_subscription = MastersSubscriptionSerializer(required=False)

    class Meta:
        model = Users
        exclude = ('password', 'role')


class EditMasterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    specializations = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )
    location = LocationSerializer(required=False)
    phone_numbers = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    description = serializers.CharField(required=False)



