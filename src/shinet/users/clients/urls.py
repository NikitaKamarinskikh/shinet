from django.urls import path
from . import views


urlpatterns = [
    path('', views.ClientDetailAPIView.as_view()),
    path('/delete', views.DeleteClientAPIView.as_view()),
    path('/edit', views.EditClientAPIView.as_view()),
]


