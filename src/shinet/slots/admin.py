from django.contrib import admin
from . import models


@admin.register(models.Slots)
class SlotsAdmin(admin.ModelAdmin):
    list_display = ('master', 'start_datetime', 'end_datetime')

    class Meta:
        model = models.Slots
