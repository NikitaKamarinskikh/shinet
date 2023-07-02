from django.contrib import admin
from . import models


@admin.register(models.VerificationCodes)
class VerificationCodesAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'expiration_time')

    class Meta:
        model = models.VerificationCodes


@admin.register(models.Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'role', 'email', 'status', 'created_at')
    list_filter = ('role', )
    search_fields = ('first_name', 'last_name', 'email')
    list_display_links = ('first_name', 'last_name', 'email')

    class Meta:
        model = models.Users


@admin.register(models.MasterInfo)
class MasterInfoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'uuid', 'rating')
    list_display_links = ('pk', 'uuid')

    class Meta:
        model = models.MasterInfo


@admin.register(models.Locations)
class LocationsAdmin(admin.ModelAdmin):
    list_display = ('city', 'district', 'street', 'house', 'office', 'floor')

    class Meta:
        model = models.Locations


@admin.register(models.UserSettings)
class UsersSettingsAdmin(admin.ModelAdmin):

    class Meta:
        model = models.UserSettings


@admin.register(models.UsersPhonesNumbers)
class UsersPhonesNumbersAdmin(admin.ModelAdmin):

    class Meta:
        model = models.UsersPhonesNumbers


@admin.register(models.UnregisteredClients)
class UnregisteredClientsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')

    class Meta:
        model = models.UnregisteredClients
