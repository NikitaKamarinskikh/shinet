from django.urls import path
from . import views


urlpatterns = [
    path('', views.SlotsListAPIView.as_view()),
    path('create/', views.CreateSlotAPIView.as_view()),
]

