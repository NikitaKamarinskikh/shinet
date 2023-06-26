"""

"""
from __future__ import annotations
import json
import logging
from typing import List, Dict, Any
from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from django.db.models import Prefetch

from slots.models import Slots
from slots.services import get_slots_with_bookings_by_date_range_and_master_id, get_slots_by_date_range_and_master_id, get_bookings_by_slot_id
from slots import serializers

SCHEDULE_KEY = 'schedule'
UNREAD_MESSAGES_QUANTITY_KEY = 'unread_messages'


class SlotConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._keys = []

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'slots_{self.room_name}'

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
            request = json.loads(text_data)
            await self._process_input_request(request)
        except Exception as e:
            logging.exception(e)

    async def notify_master_about_new_booking(self, event):
        print(event['instance'])
        await self._process_input_request(None)

    async def _process_input_request(self, request):
        response_data = dict()
        if request is not None:
            self._keys = request.keys()
        if SCHEDULE_KEY in self._keys:
            parameters = None
            if request is not None:
                parameters = request.get(SCHEDULE_KEY)
            response_data[SCHEDULE_KEY] = await self._collect_schedule_data(parameters)
        if UNREAD_MESSAGES_QUANTITY_KEY in self._keys:
            response_data[UNREAD_MESSAGES_QUANTITY_KEY] = await self._count_unread_messages()
        await self._answer(response_data)

    async def _answer(self, response_data: Dict[str, Any]):
        await self.send(text_data=json.dumps(
            response_data
        ))

    async def _collect_schedule_data(self, parameters: Dict[str, Any] | None) -> Dict[str, Any]:
        if parameters is not None:
            start_date_str = parameters.get('start_date')
            end_date_str = parameters.get('end_date')

            if start_date_str is not None:
                self.schedule_start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                self.schedule_end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        slots = await sync_to_async(get_slots_with_bookings_by_date_range_and_master_id)(
            self.room_name, self.schedule_start_date, self.schedule_end_date
        )
        serializer = serializers.SocketSlotSerializer(slots, many=True)
        return serializer.data

    async def _count_unread_messages(self) -> int:
        return 999

