from django.contrib import admin
from .models import Users


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'role', 'email', 'created_at')
    list_filter = ('role', )
    search_fields = ('first_name', 'last_name', 'email')
    list_display_links = ('first_name', 'last_name')

    class Meta:
        model = Users

