from django.db import models
from users.models import MasterInfo


class Slots(models.Model):
    master = models.ForeignKey(MasterInfo, verbose_name='Master', on_delete=models.PROTECT)
    start_datetime = models.DateTimeField(verbose_name='Start datetime')
    end_datetime = models.DateTimeField(verbose_name='End datetime')

    def __str__(self):
        return f'{self.master} slot from {self.start_datetime} to {self.end_datetime}'

    class Meta:
        verbose_name = 'Slot'
        verbose_name_plural = 'Slots'



