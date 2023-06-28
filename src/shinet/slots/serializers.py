from rest_framework import serializers

from services.serializers import MasterServiceSerializer
from users.clients.serializers import BaseClientSerializer
from . import models


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Bookings


class SlotSerializer(serializers.ModelSerializer):
    bookings = BookingSerializer(many=True)

    class Meta:
        model = models.Slots
        fields = '__all__'


class SocketSlotSerializer(serializers.ModelSerializer):
    bookings_list = BookingSerializer(many=True)

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


class GenerateSlotsQuerySerializer(serializers.Serializer):
    date = serializers.DateField(format='%Y-%m-%d')
    start_time = serializers.TimeField(format='%H:%M')
    end_time = serializers.TimeField(format='%H:%M')
    duration_in_minutes = serializers.IntegerField()
    interval_in_minutes = serializers.IntegerField(required=False)


class BookSlotSerializer(serializers.Serializer):
    slot_id = serializers.IntegerField()
    service_id = serializers.IntegerField()
    client_id = serializers.IntegerField()
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()
    client_comment = serializers.CharField(required=False)


class BookingDetailSerializer(serializers.ModelSerializer):
    service = MasterServiceSerializer()
    client = BaseClientSerializer()

    class Meta:
        model = models.Bookings
        fields = '__all__'


class UnregisteredBookingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.UnregisteredClientsBookings

