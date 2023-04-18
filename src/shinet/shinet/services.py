"""
This module contains additional settings and functions for all another apps
"""
from typing import Tuple, Dict
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status


def make_422_response(errors: Dict[str, str]) -> Response:
    """
    Format errors for struct like this:
    {
        'errors': [
            {
                'field': 'email',
                'message': 'Email already in use'
            }
        ]
    }
    """
    response_errors = [
        {
            'field': field,
            'message': message
        }
        for field, message in errors.items()
    ]
    return Response(
        data={
            'errors': response_errors
        },
        status=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


HTTP_422_RESPONSE_SWAGGER_SCHEME = \
    openapi.Response(
        description="Bad request",
        schema=openapi.Schema(
            type='object',
            properties={
                'errors': openapi.Schema(
                    type='array',
                    items=openapi.Schema(
                        type='object',
                        properties={
                            'field': openapi.Schema(type='string'),
                            'message': openapi.Schema(type='string'),
                        }
                    )
                )
            }
        )
    )