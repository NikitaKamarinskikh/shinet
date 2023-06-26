from django.urls import path

from slots.consumers import SlotConsumer


websocket_urlpatterns = [
    path('ws/<str:user_id>/', SlotConsumer.as_asgi()),
]


