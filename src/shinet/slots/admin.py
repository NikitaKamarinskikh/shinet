from django.contrib import admin
from . import models


@admin.register(models.Slots)
class SlotsAdmin(admin.ModelAdmin):
    list_display = ('master', 'start_datetime', 'end_datetime')

    class Meta:
        model = models.Slots


@admin.register(models.Bookings)
class BookingsAdmin(admin.ModelAdmin):
    list_display = ('slot', 'service', 'client', 'start_datetime', 'end_datetime')

    class Meta:
        model = models.Bookings

