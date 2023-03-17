from django.urls import path
from .clients_views import ClientsRegistrationAPIView
from .masters_views import MastersRegistrationAPIView

urlpatterns = [
    path('masters/registration/', MastersRegistrationAPIView.as_view()),
    path('clients/registration/', ClientsRegistrationAPIView.as_view()),
]

