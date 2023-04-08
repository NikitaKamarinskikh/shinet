from django.urls import path
from .views import LocationsAPIView

urlpatterns = [
    path('', LocationsAPIView.as_view()),
]
