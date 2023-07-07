from __future__ import annotations
from typing import Optional, Dict, Any, List
from random import randint

import json
import hmac
import hashlib
from base64 import urlsafe_b64encode, urlsafe_b64decode
from django.core.mail import send_mail
from django.conf import settings

from shinet.settings import env
from users.models import Users
from users.settings import UsersStatuses
from .models import VerificationCodes, VerificationTokens


def get_user_by_email_or_none(email: str) -> Optional[Users]:
    """Check user with `email` exists in `Users` model
    """
    return Users.objects.filter(email=email).first()


def send_verification_code(email: str, code: int) -> int:
    """Send code to email
    :param email:
    :param code:
    :return:
    """
    return send_mail(
        'Shinet verification',
        f'Use {code} code to verify your email',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


def create_verification_code(email: str, code: int) -> VerificationCodes:
    """Save verification code and emal to database
    :type email: str
    :param email: user email
    :type email: str
    :param code: randomly generated unique digit
    :type code: int
    :raises IntegrityError: if email or code already exist in the table
    :return: instance of RegistrationVerificationCodes or RecoverVerificationCodes class
    """
    return VerificationCodes.objects.create(email=email, code=code)


def create_or_replace_verification_code(email: str, code: int) -> VerificationCodes:
    """

    """
    current_code = get_verification_code_by_code_or_none(code)
    if current_code is not None:
        current_code.code = code
        current_code.save()
    else:
        current_code = create_verification_code(email, code)
    return current_code


def get_verification_code_by_code_or_none(code: int) -> Optional[VerificationCodes]:
    """Get instance of VerificationCodes if exists. Otherwise, returns None
    :param code: code from request
    :return: VerificationCodes or None
    """
    return VerificationCodes.objects.filter(code=code).first()


def get_verification_code_by_email_or_none(email: str) -> Optional[VerificationCodes]:
    """Get instance of VerificationCodes if exists. Otherwise, returns None
    :param email: email from request
    :return: VerificationCodes or None
    """
    return VerificationCodes.objects.filter(email=email).first()


def get_verification_code_by_code_and_email_or_none(email: str, code: int) -> VerificationCodes:
    """Search verification code by email and code
    :param code: current code
    :param email: user email
    :return: VerificationCodes or None
    """
    return VerificationCodes.objects.filter(code=code, email=email).first()


def update_verification_code_by_email(email: str, new_code: int) -> VerificationCodes:
    """Update existing record of verification code.
    :param new_code: new unique code
    :param email: user email
    :raises VerificationCodes.DoesNotExist: if records does not exists
    :return: instance of VerificationCodes class with new code
    """
    current_code = VerificationCodes.objects.get(email=email)
    current_code.code = new_code
    current_code.save()
    return current_code


def create_unique_code() -> int:
    """Create unique code
    :return: unique code
    """
    current_codes = VerificationCodes.objects.values_list('code', flat=True)
    while True:
        code = randint(100000, 999999)
        if code not in current_codes:
            return code


def is_verification_code_exists(*, code: int = None, email: str = None) -> bool:
    """Check verification code exists in database
    If `code` is not None, check by code
    If `email` is not None, check by email
    If both are None raises `ValueError`
    """
    if code is None and email is None:
        raise ValueError('You should specify `code` or `email` to call this function')
    if code is not None:
        return get_verification_code_by_code_or_none(code) is not None
    return get_verification_code_by_email_or_none(email) is not None


def is_user_blocked(user_id: int) -> bool:
    """Check is master or client blocked
    :param user_id: id of user
    :raises Users.DoesNotExist: if user does not exists
    :return: True if user blocked else False
    """
    user = Users.objects.get(pk=user_id)
    return user.status == UsersStatuses.BLOCKED.value


def create_verification_token(email: str, token: str) -> VerificationTokens:
    return VerificationTokens.objects.create(email=email, token=token)


def create_or_replace_verification_token(email: str, token: str) -> VerificationTokens:
    current_token = get_verification_token_by_email_and_token_or_none(email, token)
    if current_token is not None:
        current_token.token = token
        current_token.save()
    else:
        current_token = create_verification_token(email, token)
    return current_token


def get_verification_token_by_email_and_token_or_none(email: str, token: str) -> VerificationTokens:
    return VerificationTokens.objects.filter(email=email, token=token).first()


def generate_verification_token(data: Dict[Any, Any]) -> str:
    token_secret = env.str('VERIFICATION_TOKEN_SECRET_KEY')
    str_data = json.dumps(data)
    encoded_data = base64_url_encode(str_data)
    signature = hmac.new(token_secret.encode(), encoded_data.encode(), hashlib.sha256).hexdigest()
    token = f"{encoded_data}.{signature}"
    return token





def base64_url_encode(data: str) -> str:
    d = data.encode('utf-8')
    return urlsafe_b64encode(d).rstrip(b'=').decode('utf-8')


def base64_url_decode(data: str) -> str:
    padding = b'=' * (4 - (len(data) % 4))
    d = data.encode('utf-8')
    return urlsafe_b64decode(d + padding).decode('utf-8')




