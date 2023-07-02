from django.urls import path
from . import views


urlpatterns = [
    path('', views.ClientDetailAPIView.as_view()),
]


