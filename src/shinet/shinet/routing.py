from django.urls import path

from slots.consumers import SlotConsume


websocket_urlpatterns = [
    path('ws/<str:>/', SlotConsume.as_asgi()),
]


