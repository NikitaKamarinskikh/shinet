from django.contrib import admin
from .models import VerificationCodes


@admin.register(VerificationCodes)
class VerificationCodesAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'expiration_time')

    class Meta:
        model = VerificationCodes

