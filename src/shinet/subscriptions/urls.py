from django.urls import path
from . import views


urlpatterns = [
    path('', views.SubscriptionListAPIView.as_view()),
    path('history/', views.SubscriptionsHistoryAPIView.as_view()),
    path('pay/', views.SubscriptionsPaymentAPIView.as_view()),
]

