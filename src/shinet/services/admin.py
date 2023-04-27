from django.contrib import admin
from .models import Specializations, Services


@admin.register(Specializations)
class SpecializationsAdmin(admin.ModelAdmin):
    list_display = ('name', )

    class Meta:
        model = Specializations


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('specialization', 'name', 'price')

    class Meta:
        model = Services





