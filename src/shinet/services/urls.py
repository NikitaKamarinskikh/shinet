from django.urls import path
from . import views


urlpatterns = [
    path('', views.MastersServicesListAPIView.as_view()),
    path('add/', views.AddMasterServiceAPIView.as_view()),
    path('edit/', views.EditMasterServiceAPIView.as_view()),
    path('delete/<int:service_id>/', views.DeleteMasterServiceAPIView.as_view()),
    path('specializations/', views.SpecializationsAPIView.as_view())
]

