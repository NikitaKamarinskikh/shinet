from django.urls import path
from . import views

urlpatterns = [
    path('', views.UnregisteredClientsListAPIView.as_view()),
    path('add/', views.CreateUnregisteredClientAPIView.as_view()),
    path('<int:unregistered_client_id>/', views.DetailUnregisteredClientAPIView.as_view()),
]



