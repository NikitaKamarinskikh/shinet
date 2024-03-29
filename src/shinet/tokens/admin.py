from django.contrib import admin
from .models import RefreshTokens


@admin.register(RefreshTokens)
class RefreshTokensAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')

    class Meta:
        model = RefreshTokens

