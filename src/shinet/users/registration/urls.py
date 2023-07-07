from django.urls import path

from .views import MastersRegistrationAPIView, ClientsRegistrationAPIView


urlpatterns = [
    path('master/', MastersRegistrationAPIView.as_view()),
    path('client/', ClientsRegistrationAPIView.as_view()),
]


