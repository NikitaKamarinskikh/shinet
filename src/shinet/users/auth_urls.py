from django.urls import path
from .common.views import UserAuthenticationAPIView,SendVerificationCodeAPIView, VerifyCodeAPIView,\
    UpdateVerificationCodeAPIView


urlpatterns = [
    path('', UserAuthenticationAPIView.as_view()),
    path('send_verification_code/', SendVerificationCodeAPIView.as_view()),
    path('verify_code/', VerifyCodeAPIView.as_view()),
    path('update_verification_code/', UpdateVerificationCodeAPIView.as_view())
]
