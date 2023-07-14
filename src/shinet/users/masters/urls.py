from django.urls import path

from . import views

urlpatterns = [
    path('', views.MasterDetailAPIView.as_view()),
    path('edit/', views.EditMasterAPIView.as_view()),
]

