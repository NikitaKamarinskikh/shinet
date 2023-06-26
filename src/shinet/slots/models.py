from django.db import models
from users.models import MasterInfo
from services.models import Services
from users.models import Users, UnregisteredClients


class Slots(models.Model):
    master = models.ForeignKey(MasterInfo, verbose_name='Master', on_delete=models.PROTECT)
    start_datetime = models.DateTimeField(verbose_name='Start datetime')
    end_datetime = models.DateTimeField(verbose_name='End datetime')

    def __str__(self):
        return f'{self.master} slot from {self.start_datetime} to {self.end_datetime}'

    class Meta:
        verbose_name = 'Slot'
        verbose_name_plural = 'Slots'


class Bookings(models.Model):
    slot = models.ForeignKey(Slots, verbose_name='Slot', on_delete=models.PROTECT, related_name='bookings')
    service = models.ForeignKey(Services, verbose_name='Service', on_delete=models.PROTECT)
    client = models.ForeignKey(Users, verbose_name='Client', on_delete=models.CASCADE)
    start_datetime = models.DateTimeField(verbose_name='Start datetime')
    end_datetime = models.DateTimeField(verbose_name='End datetime')

    def __str__(self):
        return f'{self.pk} {self.start_datetime} {self.end_datetime}'

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'




