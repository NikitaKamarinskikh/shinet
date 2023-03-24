"""
This module contains additional functions for emails app
"""
from __future__ import annotations
from random import randint
from .models import VerificationCodes
from django.core.mail import send_mail
from django.conf import settings


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


def save_verification_code(email: str, code: int) -> VerificationCodes:
    """Save verification code and emal to database
    :param email: user email
    :type email: str
    :param code: randomly generated unique digit
    :type code: int
    :raises IntegrityError: if email or code already exist in the table
    :return: instance of VerificationCodes class
    """
    return VerificationCodes.objects.create(email=email, code=code)


def get_verification_code_by_code_or_none(code: int) -> VerificationCodes | None:
    """Get instance of VerificationCodes if exists. Otherwise, returns None
    :param code: code from request
    :return: VerificationCodes or None
    """
    return VerificationCodes.objects.filter(code=code).first()


def get_verification_code_by_code_and_email_or_none(
                email: str, code: int) -> VerificationCodes | None:
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




