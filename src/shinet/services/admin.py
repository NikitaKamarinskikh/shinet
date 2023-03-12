from django.contrib import admin
from .models import Specializations, Services, ServiceImages


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


@admin.register(ServiceImages)
class ServiceImagesAdmin(admin.ModelAdmin):
    list_display = ('service', )

    class Meta:
        model = ServiceImages




