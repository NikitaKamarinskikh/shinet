
from django.urls import path
from .views import IsEmailAvailableAPIView, SendCodeAPIView, VerifyCodeAPIView, UpdateCodeAPIView


urlpatterns = [
    path('isavailable/', IsEmailAvailableAPIView.as_view()),
    path('send_code', SendCodeAPIView.as_view()),
    path('verify_code/', VerifyCodeAPIView.as_view()),
    path('update/', UpdateCodeAPIView.as_view())
]

