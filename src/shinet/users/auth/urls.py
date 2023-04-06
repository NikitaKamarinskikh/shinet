from django.urls import path
from .views import UserAuthenticationAPIView

urlpatterns = [
  path('', UserAuthenticationAPIView.as_view()),
]


