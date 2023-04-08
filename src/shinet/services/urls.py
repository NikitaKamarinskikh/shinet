from django.urls import path
from .views import SpecializationsAPIView


urlpatterns = [
    path('specializations/', SpecializationsAPIView.as_view())
]

