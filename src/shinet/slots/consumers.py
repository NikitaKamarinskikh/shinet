"""

"""
from __future__ import annotations
import json
import logging
from collections import OrderedDict
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
        print('Instance:', event['instance'])
        await self._process_input_request(event)

    async def _process_input_request(self, request):
        print('request', request)
        response_data = dict()
        if request is not None:
            if not request.get('save_keys'):
                self._keys = request.keys()
        print('self._keys', self._keys)
        if SCHEDULE_KEY in self._keys:
            parameters = None
            if request is not None:
                if request.get(SCHEDULE_KEY):
                    parameters = request.get(SCHEDULE_KEY)
                else:
                    parameters = request
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
        items = serializer.data
        if parameters.get('type') == 'notify_master_about_new_booking':
            item_exists = False
            for item in items:
                if item.get('id') == parameters.get('instance').slot.pk:
                    item_bookings = item.get('bookings')
                    for booking in item_bookings:
                        if booking.get('id') == parameters.get('instance').pk:
                            item_exists = True
                            break
                if not item_exists:
                    instance_item = OrderedDict(
                        [
                            ('id', parameters.get('instance').pk),
                            ('start_datetime', parameters.get('instance').start_datetime.strftime('%Y-%m-%d %H:%M')),
                            ('end_datetime', parameters.get('instance').end_datetime.strftime('%Y-%m-%d %H:%M')),
                            ('client_comment', parameters.get('instance').client_comment),
                            ('slot', parameters.get('instance').slot.pk),
                            ('service', parameters.get('instance').service.pk),
                            ('client', parameters.get('instance').client.pk),
                        ]
                    )
                    item.get('bookings').append(instance_item)
                break
        return items

    async def _count_unread_messages(self) -> int:
        return 999

