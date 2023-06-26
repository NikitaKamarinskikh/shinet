from django.urls import path
from . import views


urlpatterns = [
    path('', views.SlotsListAPIView.as_view()),
    path('create/', views.CreateSlotAPIView.as_view()),
    path('book/', views.BookSlotAPIView.as_view()),
    path('booking/<int:booking_id>/', views.BookingDetailAPIView.as_view()),
]

