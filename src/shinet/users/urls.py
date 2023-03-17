from django.urls import path
from .clients.views import ClientsRegistrationAPIView
from .masters.views import MastersRegistrationAPIView

urlpatterns = [
    path('masters/registration/', MastersRegistrationAPIView.as_view()),
    path('clients/registration/', ClientsRegistrationAPIView.as_view()),
]

