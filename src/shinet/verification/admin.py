from django.contrib import admin

from . import models


@admin.register(models.VerificationCodes)
class VerificationCodesAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'expiration_time')

    class Meta:
        model = models.VerificationCodes
