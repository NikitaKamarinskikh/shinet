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
from slots import serializers
from slots import services as slots_services


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
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            request = json.loads(text_data)
            await self._process_input_request(request)
        except Exception as e:
            logging.exception(e)

    async def notify_master_about_new_booking(self, event):
        await self._process_input_request(event)

    async def _process_input_request(self, request):
        response_data = dict()
        if request is not None:
            if not request.get('save_keys'):
                self._keys = request.keys()
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

        slots = await sync_to_async(slots_services.get_slots_by_date_range_and_master_id)(
            self.room_name, self.schedule_start_date, self.schedule_end_date
        )
        for slot in slots:
            bookings_list = []
            bookings = await sync_to_async(slots_services.get_bookings_by_slot_id)(slot.pk)
            unregistered_clients_bookings =\
                await sync_to_async(slots_services.get_unregistered_clients_bookings_by_slot_id)(slot.pk)
            for booking in bookings:
                setattr(booking, 'type', 'registered_client')
                bookings_list.append(booking)
            for unregistered_client_booking in unregistered_clients_bookings:
                setattr(unregistered_client_booking, 'type', 'unregistered_client')
                bookings_list.append(unregistered_client_booking)
            setattr(slot, 'bookings_list', bookings_list)

        serializer = serializers.SocketSlotSerializer(slots, many=True)
        return serializer.data

    async def _count_unread_messages(self) -> int:
        return 999

