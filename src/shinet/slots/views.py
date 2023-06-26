import logging

from datetime import datetime, timezone
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
from .date_range import DateRange, InvalidDateRange


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


class CreateSlotAPIView(GenericAPIView):
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
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Server error'
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

        try:
            date_range = DateRange(start_datetime, end_datetime)
        except InvalidDateRange:
            return make_422_response({'start_date': 'Start date must be earlier than end date'})
        if start_datetime == end_datetime:
            return make_422_response({'end_date': 'End date must not be same as start_date'})
        if date_range.duration_in_minutes < services.MINIMAL_SLOT_TIME_IN_MINUTES:
            return make_422_response({'end_date': f'Minimal slot time is {services.MINIMAL_SLOT_TIME_IN_MINUTES} minutes'})
        if date_range.duration_in_hours > services.MAXIMAL_SLOT_TIME_IN_HOURS:
            return make_422_response({'end_date': f'Maximal slot time is {services.MAXIMAL_SLOT_TIME_IN_HOURS} hours'})
        # if start_datetime < now:
        #     return make_422_response({'start_date': 'Start date is too old'})
        # if end_datetime < now:
        #     return make_422_response({'start_date': 'End date is too old'})

        start_time_minutes_str = str(date_range.start_time).split(':')[1]
        end_time_minutes_str = str(date_range.end_time).split(':')[1]
        if int(start_time_minutes_str) % 5 != 0:
            return make_422_response({'start_date': 'Invalid start date minutes'})
        if int(end_time_minutes_str) % 5 != 0:
            return make_422_response({'end_date': 'Invalid end date minutes'})

        slots = services.get_slots_by_master_id(master_id)

        for slot in slots:
            slot_date_range = DateRange(slot.start_datetime, slot.end_datetime)
            if date_range.has_intersection(slot_date_range, include_start=False, include_end=False) or\
                    date_range.is_equal(slot_date_range):
                return make_422_response({'start_date': 'Date range intersection'})

        slot = services.create_slot(master_id, start_datetime, end_datetime)
        slot_serializer = serializers.SlotSerializer(slot)
        return Response(status=status.HTTP_200_OK, data=slot_serializer.data)


class BookSlotAPIView(GenericAPIView):
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
        new_booking_date_range = DateRange(start_datetime, end_datetime)

        current_bookings = services.get_bookings_by_slot_id(slot_id)
        for booking in current_bookings:
            booking_range = DateRange(booking.start_datetime, booking.end_datetime)
            if new_booking_date_range.has_intersection(booking_range, include_start=False, include_end=False) or\
                    new_booking_date_range.is_equal(booking_range):
                return make_422_response({'start_date': 'Date range intersection'})

        booking = services.save_booking(slot_id, service_id, client_id, start_datetime, end_datetime)
        booking_serializer = serializers.BookingSerializer(booking)
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
    # @check_access_token
    def get(self, request, booking_id: int):
        booking = services.get_booking_by_id_or_none(booking_id)
        if booking is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        client_phone_numbers = get_user_phone_numbers(booking.client.pk)
        setattr(booking.client, 'phone_numbers', client_phone_numbers)
        serializer = serializers.BookingDetailSerializer(booking)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

