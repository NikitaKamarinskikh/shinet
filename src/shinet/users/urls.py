from django.urls import path

from . import views

urlpatterns = [
    path('notifications/tokens/add/', views.AddNotificationTokenAPIView.as_view()),
    path('notifications/status/swap/', views.SwapUserNotificationStatusAPIView.as_view()),
]
