from django.contrib import admin
from .models import Users, MasterInfo, UserSettings,\
    UsersPhonesNumbers, UnregisteredClients, VerificationCodes, Locations


@admin.register(VerificationCodes)
class VerificationCodesAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'expiration_time')

    class Meta:
        model = VerificationCodes


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'role', 'email', 'status', 'created_at')
    list_filter = ('role', )
    search_fields = ('first_name', 'last_name', 'email')
    list_display_links = ('first_name', 'last_name', 'email')

    class Meta:
        model = Users


@admin.register(MasterInfo)
class MasterInfoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'uuid', 'rating')
    list_display_links = ('pk', 'uuid')

    class Meta:
        model = MasterInfo


@admin.register(Locations)
class LocationsAdmin(admin.ModelAdmin):
    list_display = ('city', 'district', 'street', 'house', 'office', 'floor')

    class Meta:
        model = Locations


@admin.register(UserSettings)
class UsersSettingsAdmin(admin.ModelAdmin):

    class Meta:
        model = UserSettings


@admin.register(UsersPhonesNumbers)
class UsersPhonesNumbersAdmin(admin.ModelAdmin):

    class Meta:
        model = UsersPhonesNumbers


@admin.register(UnregisteredClients)
class UnregisteredClientsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')

    class Meta:
        model = UnregisteredClients
