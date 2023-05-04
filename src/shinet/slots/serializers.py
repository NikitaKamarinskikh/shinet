from rest_framework import serializers
from . import models


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Slots
        fields = '__all__'


class SlotsListQuerySerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()


class CreateSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Slots
        exclude = ('master', )
