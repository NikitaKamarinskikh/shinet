
from django.urls import path
from .views import IsEmailAvailableAPIView

urlpatterns = [
    path('isavailable/', IsEmailAvailableAPIView.as_view())
]

