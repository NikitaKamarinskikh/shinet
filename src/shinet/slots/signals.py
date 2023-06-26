import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Slots, Bookings
from .serializers import BookingSerializer


@receiver(post_save, sender=Bookings)
def send_message(sender, instance: Bookings, created, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'slots_15',
        {
            'type': 'notify_master_about_new_booking',
            'instance': instance
        }
    )


