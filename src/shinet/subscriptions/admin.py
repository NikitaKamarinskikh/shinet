from django.contrib import admin
from .models import Subscriptions, MastersSubscriptions


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('type', 'price_without_discount', 'price_with_discount', 'discount_in_percent')

    class Meta:
        model = Subscriptions


@admin.register(MastersSubscriptions)
class MastersSubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('master', 'subscription', 'start_date', 'end_date', 'status')

    class Meta:
        model = MastersSubscriptions

