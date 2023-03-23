from django.urls import path
from .views import UpdateRefreshTokenAPIView


urlpatterns = [
    path('update/', UpdateRefreshTokenAPIView.as_view()),
]

