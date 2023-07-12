import logging
import hmac
import hashlib
from typing import Callable

from rest_framework.response import Response
from rest_framework import status

from shinet.settings import env


def check_verification_token(func: Callable):

    def wrapper(*args, **kwargs):
        request = args[1]
        verification_token = request.META.get('HTTP_VERIFICATION')
        secret_key = env.str('VERIFICATION_TOKEN_SECRET_KEY')
        try:
            bearer, token = verification_token.split()  # 'Bearer' {token}
            if bearer != 'Bearer':
                return Response(status=status.HTTP_403_FORBIDDEN)
            received_data, received_signature = token.split(".")
            computed_signature = hmac.new(secret_key.encode(), received_data.encode(), hashlib.sha256).hexdigest()
            if received_signature != computed_signature:
                return Response(status=status.HTTP_403_FORBIDDEN)
            return func(*args, **kwargs)
        except Exception as e:
            logging.exception(e)
            return Response(status=status.HTTP_403_FORBIDDEN)

    return wrapper


