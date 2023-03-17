from django.urls import path
from .clients_views import ClientsRegistrationAPIView

urlpatterns = [
    # path('masters/registration/', ClientsRegistrationAPIView.as_view()),
    path('clients/registration/', ClientsRegistrationAPIView.as_view()),
]

