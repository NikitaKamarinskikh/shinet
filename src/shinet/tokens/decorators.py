import logging
from typing import Callable

from rest_framework.response import Response
from rest_framework import status

from .jwt import JWT
from .exceptions import InvalidAccessTokenException
from .services import validate_access_token


def check_access_token(func: Callable):

    def wrapper(*args, **kwargs):
        request = args[1]
        access_token = request.META.get('HTTP_AUTHORIZATION')
        try:
            validate_access_token(access_token)
            return func(*args, **kwargs)
        except InvalidAccessTokenException as e:
            logging.exception(e)
            return Response(status=status.HTTP_403_FORBIDDEN)

    return wrapper


