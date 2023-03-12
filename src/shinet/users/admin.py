from django.contrib import admin
from .models import Users, UserSettings


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'role', 'email', 'created_at')
    list_filter = ('role', )
    search_fields = ('first_name', 'last_name', 'email')
    list_display_links = ('first_name', 'last_name', 'email')

    class Meta:
        model = Users


@admin.register(UserSettings)
class UsersSettingsAdmin(admin.ModelAdmin):

    class Meta:
        model = UserSettings


