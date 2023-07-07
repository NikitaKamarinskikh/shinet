from django.urls import path

from .views import RecoverPasswordAPIView

urlpatterns = [
    path('', RecoverPasswordAPIView.as_view()),
]
