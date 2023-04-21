from django.urls import path
from .views import SubscriptionListAPIView


urlpatterns = [
    path('', SubscriptionListAPIView.as_view())
]

