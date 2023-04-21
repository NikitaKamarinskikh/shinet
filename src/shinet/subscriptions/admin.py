from django.contrib import admin
from .models import Subscriptions, ActiveSubscriptions


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('type', 'price_without_discount', 'price_with_discount', 'discount_in_percent')

    class Meta:
        model = Subscriptions


@admin.register(ActiveSubscriptions)
class ActiveSubscriptionsAdmin(admin.ModelAdmin):

    class Meta:
        model = ActiveSubscriptions

