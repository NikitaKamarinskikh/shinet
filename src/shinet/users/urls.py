from django.urls import path
from .clients.views import ClientsRegistrationAPIView
from .masters.views import MastersRegistrationAPIView
from .common.views import UserAuthenticationAPIView, SendVerificationCodeAPIView, VerifyCodeAPIView,\
    UpdateVerificationCodeAPIView

urlpatterns = [
    path('masters/registration/', MastersRegistrationAPIView.as_view()),
    path('clients/registration/', ClientsRegistrationAPIView.as_view()),

    path('auth/', UserAuthenticationAPIView.as_view()),

    path('send_verification_code/', SendVerificationCodeAPIView.as_view()),
    path('verify_code/', VerifyCodeAPIView.as_view()),
    path('update_verification_code/', UpdateVerificationCodeAPIView.as_view())

]

