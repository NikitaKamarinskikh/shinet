from django.urls import path
from users.masters.views import MastersRegistrationAPIView


urlpatterns = [
    path('registration/', MastersRegistrationAPIView.as_view()),
]
