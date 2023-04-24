from rest_framework import serializers
from users.models import UnregisteredClients


class UnregisteredClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnregisteredClients
        fields = ('first_name', 'last_name', 'extra_info')


