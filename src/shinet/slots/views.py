import logging
from typing import List
from datetime import datetime, timezone, timedelta, time, date

from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from tokens.decorators import check_access_token
from tokens.services import get_payload_from_token
from shinet.services import HTTP_422_RESPONSE_SWAGGER_SCHEME, make_422_response
from users.services import get_user_phone_numbers
from . import serializers
from . import services
from .mixins import SlotsValidationMixin, BookingValidationMixin
from .date_range import DateRange, InvalidDateRangeException


class SlotsListAPIView(GenericAPIView):
    serializer_class = serializers.SlotSerializer

    @swagger_auto_schema(
        request_headers={
            'Authorization': 'Bearer <token>'
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, 'Access token',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            status.HTTP_200_OK: serializers.SlotSerializer(many=True),
            status.HTTP_403_FORBIDDEN: 'Access denied',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Server error'
        },
        operation_description='This method gets `master_id` from access_token. Date format `YYYY-MM-DD`',
        query_serializer=serializers.SlotsListQuerySerializer()
    )
    @check_access_token
    def get(self, request):
        payload = get_payload_from_token(request)
        master_id = payload.get('master_id')
        if master_id is None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        query_serializer = serializers.SlotsListQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        start_date = query_serializer.validated_data.get('start_date')
        end_date = query_serializer.validated_data.get('end_date')
        slots = services.get_slots_with_bookings_by_date_range_and_master_id(master_id, start_date, end_date)
        serializer = serializers.SlotSerializer(slots, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class CreateSlotAPIView(SlotsValidationMixin, GenericAPIView):
    serializer_class = serializers.CreateSlotSerializer

    @swagger_auto_schema(
        request_headers={
            'Authorization': 'Bearer <token>'
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, 'Access token',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            status.HTTP_200_OK: serializers.SlotSerializer(many=True),
            status.HTTP_403_FORBIDDEN: 'Access denied',
            status.HTTP_422_UNPROCESSABLE_ENTITY: HTTP_422_RESPONSE_SWAGGER_SCHEME,
        },
        operation_description='This method gets `master_id` from access_token'
    )
    @check_access_token
    def post(self, request):
        payload = get_payload_from_token(request)
        master_id = payload.get('master_id')
        if master_id is None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.CreateSlotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        start_datetime = serializer.validated_data.get('start_datetime')
        end_datetime = serializer.validated_data.get('end_datetime')

        previous_date = datetime.now() - timedelta(days=1)
        slots = services.get_slots_by_date_range_and_master_id(master_id, start_date=previous_date)

        slot_validation = self.validate_slot_dates(master_id, start_datetime, end_datetime, slots)
        if not slot_validation.is_valid():
            return make_422_response(slot_validation.errors)

        slot = services.create_slot(master_id, start_datetime, end_datetime)
        slot_serializer = serializers.SlotSerializer(slot)
        return Response(status=status.HTTP_200_OK, data=slot_serializer.data)


class GenerateSlotsAPIView(SlotsValidationMixin, GenericAPIView):
    serializer_class = serializers.GenerateSlotsQuerySerializer

    @swagger_auto_schema(
        request_headers={
            'Authorization': 'Bearer <token>'
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, 'Access token',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            status.HTTP_200_OK: serializers.SlotSerializer(many=True),
            status.HTTP_403_FORBIDDEN: 'Access denied',
            status.HTTP_422_UNPROCESSABLE_ENTITY: HTTP_422_RESPONSE_SWAGGER_SCHEME,
        },
        operation_description='This method gets `master_id` from access_token'
    )
    @check_access_token
    def post(self, request):
        payload = get_payload_from_token(request)
        master_id = payload.get('master_id')
        if master_id is None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.GenerateSlotsQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        start_date = serializer.validated_data.get('start_date')
        end_date = serializer.validated_data.get('end_date')
        start_time = serializer.validated_data.get('start_time')
        end_time = serializer.validated_data.get('end_time')

        previous_date = datetime.now() - timedelta(days=1)
        slots = services.get_slots_by_date_range_and_master_id(master_id, start_date=previous_date)

        try:
            date_ranges = self._create_date_ranges(start_date, end_date, start_time, end_time)
        except InvalidDateRangeException:
            return make_422_response({'start_date': 'Invalid start date'})
        for date_range in date_ranges:
            validation_result = self.validate_slot_dates(
                master_id,
                date_range.start_datetime,
                date_range.end_datetime,
                slots
            )
            if not validation_result.is_valid():
                return make_422_response(validation_result.errors)

        slots =  services.create_slots(master_id, date_ranges, return_instances=True)
        response_serializer = serializers.SlotSerializer(slots, many=True)
        return Response(status=status.HTTP_200_OK, data=response_serializer.data)

    def _create_date_ranges(self, start_date: date, end_date, start_time: time, end_time: time) -> List[DateRange]:
        date_ranges: List[DateRange] = list()

        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        start_time_str = start_time.strftime('%H:%M')
        end_time_str = end_time.strftime('%H:%M')

        start_datetime = datetime.strptime(f'{start_date_str} {start_time_str}', '%Y-%m-%d %H:%M')
        end_datetime = datetime.strptime(f'{end_date_str} {end_time_str}', '%Y-%m-%d %H:%M')

        current_datetime = start_datetime
        while current_datetime < end_datetime:
            current_time_end = datetime.strptime(f'{current_datetime.strftime("%Y-%m-%d")} {end_time_str}', '%Y-%m-%d %H:%M')
            date_ranges.append(
                DateRange(
                    current_datetime,
                    current_time_end
                )
            )
            current_datetime += timedelta(days=1)

        return date_ranges


class BookSlotAPIView(BookingValidationMixin, GenericAPIView):
    serializer_class = serializers.BookSlotSerializer

    @swagger_auto_schema(
        request_headers={
            'Authorization': 'Bearer <token>'
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, 'Access token',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            status.HTTP_200_OK: serializers.BookingSerializer(),
            status.HTTP_403_FORBIDDEN: 'Access denied',
            status.HTTP_422_UNPROCESSABLE_ENTITY: HTTP_422_RESPONSE_SWAGGER_SCHEME,
        },
        operation_description=''
    )
    @check_access_token
    def post(self, request):
        serializer = serializers.BookSlotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        slot_id = serializer.validated_data.get('slot_id')
        service_id = serializer.validated_data.get('service_id')
        client_id = serializer.validated_data.get('client_id')

        start_datetime = serializer.validated_data.get('start_datetime')
        end_datetime = serializer.validated_data.get('end_datetime')

        bookings = services.get_bookings_by_slot_id(slot_id)
        unregistered_clients_bookings = services.get_unregistered_clients_bookings_by_slot_id(slot_id)

        booking_validation = self.validate_booking_time(
            start_datetime, end_datetime, bookings, unregistered_clients_bookings
        )
        if not booking_validation.is_valid():
            return make_422_response(booking_validation.errors)

        booking = services.save_booking(slot_id, service_id, client_id, start_datetime, end_datetime)
        booking_serializer = serializers.BookingSerializer(booking)
        return Response(status=status.HTTP_200_OK, data=booking_serializer.data)


class BookSlotForUnregisteredClient(BookingValidationMixin, GenericAPIView):
    serializer_class = serializers.UnregisteredBookingSerializer

    @swagger_auto_schema(
        request_headers={
            'Authorization': 'Bearer <token>'
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, 'Access token',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            status.HTTP_200_OK: serializers.UnregisteredBookingSerializer(),
            status.HTTP_403_FORBIDDEN: 'Access denied',
            status.HTTP_422_UNPROCESSABLE_ENTITY: HTTP_422_RESPONSE_SWAGGER_SCHEME,
        },
        operation_description=''
    )
    @check_access_token
    def post(self, request):
        serializer = serializers.UnregisteredBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        slot_id = serializer.validated_data.get('slot_id')
        service_id = serializer.validated_data.get('service_id')
        client_id = serializer.validated_data.get('client_id')
        start_datetime = serializer.validated_data.get('start_datetime')
        end_datetime = serializer.validated_data.get('end_datetime')

        bookings = services.get_bookings_by_slot_id(slot_id)
        unregistered_clients_bookings = services.get_unregistered_clients_bookings_by_slot_id(slot_id)

        booking_validation = self.validate_booking_time(
            start_datetime, end_datetime, bookings, unregistered_clients_bookings
        )
        if not booking_validation.is_valid():
            return make_422_response(booking_validation.errors)

        booking = services.save_unregistered_client_booking(
            slot_id, service_id, client_id, start_datetime, end_datetime
        )
        booking_serializer = serializers.UnregisteredBookingSerializer(booking)
        return Response(status=status.HTTP_200_OK, data=booking_serializer.data)


class BookingDetailAPIView(GenericAPIView):
    serializer_class = serializers.BookingDetailSerializer

    @swagger_auto_schema(
        request_headers={
            'Authorization': 'Bearer <token>'
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, 'Access token',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            status.HTTP_200_OK: serializers.BookingDetailSerializer(),
            status.HTTP_403_FORBIDDEN: 'Access denied',
            status.HTTP_404_NOT_FOUND: 'Booking not found',
            status.HTTP_422_UNPROCESSABLE_ENTITY: HTTP_422_RESPONSE_SWAGGER_SCHEME,
        },
        operation_description=''
    )
    @check_access_token
    def get(self, request, booking_id: int):
        booking = services.get_booking_by_id_or_none(booking_id)
        if booking is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        client_phone_numbers = get_user_phone_numbers(booking.client.pk)
        setattr(booking.client, 'phone_numbers', client_phone_numbers)
        serializer = serializers.BookingDetailSerializer(booking)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


