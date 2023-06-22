"""

"""
import json
import logging

from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class SlotConsume(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'slots_{self.room_name}'

        print(self.room_name, self.room_group_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        print(f'disconnected group {self.room_group_name} with code {code}')
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print('text data:', text_data)
        try:
            data = json.loads(text_data)
            print('json data:', data)
            await self.send(
                text_data=json.dumps(
                    {
                        'message': 'here is message text',
                        'keys': ['schedule', 'chat', 'other_key']
                    }
                )
            )
        except Exception as e:
            logging.exception(e)




