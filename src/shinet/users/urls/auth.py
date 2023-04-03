from django.urls import path
from users.common.views import UserAuthenticationAPIView,SendVerificationCodeAPIView, VerifyCodeAPIView,\
    UpdateVerificationCodeAPIView


urlpatterns = [
    path('', UserAuthenticationAPIView.as_view()),
    path('send-verification-code/', SendVerificationCodeAPIView.as_view()),
    path('verify-code/', VerifyCodeAPIView.as_view()),
    path('update-verification-code/', UpdateVerificationCodeAPIView.as_view())
]
