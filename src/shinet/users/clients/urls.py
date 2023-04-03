from django.urls import path
from users.clients.views import ClientsRegistrationAPIView


urlpatterns = [
    path('registration/', ClientsRegistrationAPIView.as_view()),
]
