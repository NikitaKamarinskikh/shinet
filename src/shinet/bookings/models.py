from django.db import models
from slots.services import Slots
from services.models import Services
from users.models import Users


class Bookings(models.Model):
    slot = models.ForeignKey(Slots, verbose_name='Slot', on_delete=models.PROTECT)
    service = models.ForeignKey(Services, verbose_name='Service', on_delete=models.PROTECT)
    client = models.ForeignKey(Users, verbose_name='Client', on_delete=models.CASCADE)
    start_datetime = models.DateTimeField(verbose_name='Start datetime')
    end_datetime = models.DateTimeField(verbose_name='End datetime')

    def __str__(self):
        return f'{self.client} for {self.service} of {self.slot}'

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'


