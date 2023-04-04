from django.urls import path
from users.common.views import UserAuthenticationAPIView,SendVerificationCodeAPIView, VerifyCodeAPIView,\
    UpdateVerificationCodeAPIView


urlpatterns = [
    path('', UserAuthenticationAPIView.as_view()),
    path('codes/send/', SendVerificationCodeAPIView.as_view()),
    path('codes/verify/', VerifyCodeAPIView.as_view()),
    path('codes/update/', UpdateVerificationCodeAPIView.as_view())
]
