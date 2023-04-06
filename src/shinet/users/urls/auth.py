from django.urls import path
from users.common.views import UserAuthenticationAPIView

urlpatterns = [
    path('', UserAuthenticationAPIView.as_view()),
]
