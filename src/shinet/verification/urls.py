from django.urls import path

from . import views


urlpatterns = [
    path('/codes/send', views.SendVerificationCodeAPIView.as_view()),
    path('/codes/verify', views.VerifyCodeAPIView.as_view()),
]

