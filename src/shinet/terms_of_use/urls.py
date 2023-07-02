from django.urls import path
from .views import TermsOfUseAPIView

urlpatterns = [
    path('', TermsOfUseAPIView.as_view())
]

