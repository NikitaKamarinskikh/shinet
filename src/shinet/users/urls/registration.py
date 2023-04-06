from django.urls import path
from users.masters.views import MastersRegistrationAPIView
from users.clients.views import ClientsRegistrationAPIView
from users.common.views import SendVerificationCodeAPIView, VerifyCodeAPIView,\
    UpdateVerificationCodeAPIView

urlpatterns = [
    path('master/', MastersRegistrationAPIView.as_view()),
    path('client/', ClientsRegistrationAPIView.as_view()),
    path('codes/send/', SendVerificationCodeAPIView.as_view()),
    path('codes/verify/', VerifyCodeAPIView.as_view()),
    path('codes/update/', UpdateVerificationCodeAPIView.as_view())
]


