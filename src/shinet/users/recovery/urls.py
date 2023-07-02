from django.urls import path
from users.verification.views import SendVerificationCodeAPIView, VerifyCodeAPIView,\
    UpdateVerificationCodeAPIView
from .views import RecoverPasswordAPIView

urlpatterns = [
    path('', RecoverPasswordAPIView.as_view()),
    path('codes/send/', SendVerificationCodeAPIView.as_view()),
    path('codes/verify/', VerifyCodeAPIView.as_view()),
    path('codes/update/', UpdateVerificationCodeAPIView.as_view())
]
