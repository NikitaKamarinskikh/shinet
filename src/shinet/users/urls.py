from django.urls import path

from . import views

urlpatterns = [
    path('/notifications/tokens/add', views.AddNotificationTokenAPIView.as_view()),
    path('/notifications/status/swap', views.SwapUserNotificationStatusAPIView.as_view()),
    path('/edit/email', views.EditUserEmailAPIView.as_view()),
    path('/edit/password', views.EditUserPasswordAPIView.as_view()),
]

