from django.urls import path

from websockets.consumers import Consumer


websocket_urlpatterns = [
    path('ws/<str:access_token>/', Consumer.as_asgi()),
]


