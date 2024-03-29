"""
This module contains function to manage RefreshTokens model
"""
import logging

from django.http import HttpRequest

from .exceptions import InvalidAccessTokenException
from .models import RefreshTokens
from .jwt import JWT


def create_refresh_token(user_id: int, token: str) -> RefreshTokens:
    """Save refresh token to database
    :param user_id: user id
    :type user_id: int
    :param token: refresh token string
    :type token: str
    :return: instance of RefreshTokens ORM object
    :rtype: RefreshTokens
    """
    return RefreshTokens.objects.create(user_id=user_id, token=token)


def update_refresh_token(user_id: int, token: str) -> RefreshTokens:
    """Update existing record in the database
    :param user_id: path to the file with questions
    :type user_id: int
    :param token: refresh token string
    :type token: str
    :raises RefreshTokens.DoesNotExists: if token does not store in the database
    :return: instance of RefreshTokens ORM object with new refresh token
    :rtype: RefreshTokens
    """
    current_token = get_refresh_token(user_id)
    current_token.token = token
    current_token.save()
    return current_token


def create_or_update_refresh_token(user_id: int, token: str) -> RefreshTokens:
    """Update existing record in the database if record exists
            otherwise create new record
    :param user_id: path to the file with questions
    :type user_id: int
    :param token: refresh token string
    :type token: str
    :raises RefreshTokens.DoesNotExists: if record does not store in the database
    :return: instance of RefreshTokens ORM object with new refresh token
    :rtype: RefreshTokens
    """
    current_token = get_refresh_token_or_none(user_id)
    if current_token is None:
        return create_refresh_token(user_id, token)
    return update_refresh_token(user_id, token)


def get_refresh_token(user_id: int) -> RefreshTokens:
    """Get record from RefreshTokens model
    :param user_id: user id
    :type user_id: int
    :raises RefreshTokens.DoesNotExists: if record does not store in the database
    :return: instance of RefreshTokens ORM object
    :rtype: RefreshTokens
    """
    return RefreshTokens.objects.get(user_id=user_id)


def get_refresh_token_or_none(user_id: int) -> RefreshTokens:
    """Get record from RefreshTokens model. If record does not exist returns None
    :param user_id: user id
    :type user_id: int
    :return: instance of RefreshTokens ORM object or None if record does not exist
    :rtype: RefreshTokens or None
    """
    return RefreshTokens.objects.filter(user_id=user_id).first()


def delete_refresh_token_if_exists(user_id: int) -> None:
    """Delete record of token
    :param user_id: user id
    :type user_id: int
    :return: Nothing
    :rtype: None
    """
    current_token = get_refresh_token_or_none(user_id)
    if current_token is not None:
        current_token.delete()


def get_payload_from_access_token(request: HttpRequest) -> dict:
    """
    :raises InvalidAccessTokenException:
    """
    auth_token = request.META.get('HTTP_AUTHORIZATION')
    _, access_token = auth_token.split()
    jwt = JWT(access_token)
    return jwt.payload


def validate_access_token(access_token: str) -> None:
    try:
        bearer, token = access_token.split()  # 'Bearer' {token}
        if bearer != 'Bearer':
            raise InvalidAccessTokenException()
        jwt = JWT(token)
        check_jwt = JWT(jwt.payload)
        if not check_jwt.is_equal_signature(jwt):
            raise InvalidAccessTokenException()
        if not jwt.is_available():
            raise InvalidAccessTokenException()
    except Exception as e:
        logging.exception(e)
        raise InvalidAccessTokenException()

