from django.contrib import admin
from .models import Users, MasterInfo, UserSettings,\
    UsersImages, UsersPhonesNumbers, UnregisteredClients


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'role', 'email', 'created_at')
    list_filter = ('role', )
    search_fields = ('first_name', 'last_name', 'email')
    list_display_links = ('first_name', 'last_name', 'email')

    class Meta:
        model = Users


@admin.register(MasterInfo)
class MasterInfoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'location', 'rating')

    class Meta:
        model = MasterInfo


@admin.register(UserSettings)
class UsersSettingsAdmin(admin.ModelAdmin):

    class Meta:
        model = UserSettings


@admin.register(UsersImages)
class UserImagesAdmin(admin.ModelAdmin):

    class Meta:
        model = UsersImages


@admin.register(UsersPhonesNumbers)
class UsersPhonesNumbersAdmin(admin.ModelAdmin):

    class Meta:
        model = UsersPhonesNumbers


@admin.register(UnregisteredClients)
class UnregisteredClientsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')

    class Meta:
        model = UnregisteredClients
