from django.urls import path
from users.masters.views import MastersRegistrationAPIView
from users.clients.views import ClientsRegistrationAPIView


urlpatterns = [
    path('master/', MastersRegistrationAPIView.as_view()),
    path('client/', ClientsRegistrationAPIView.as_view()),
]


