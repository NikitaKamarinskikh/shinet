from django.contrib import admin
from . import models


@admin.register(models.Bookings)
class BookingsAdmin(admin.ModelAdmin):
    list_display = ('service', 'client', 'start_datetime', 'end_datetime')

    class Meta:
        model = models.Bookings

