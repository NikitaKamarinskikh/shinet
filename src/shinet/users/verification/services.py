from __future__ import annotations
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from users.models import Users, VerificationCodes
from users.settings import UsersStatuses


def get_user_by_email_or_none(email: str) -> Users | None:
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


def save_verification_code(email: str, code: int) -> VerificationCodes:
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


def get_verification_code_by_code_or_none(code: int) -> VerificationCodes | None:
    """Get instance of VerificationCodes if exists. Otherwise, returns None
    :param code: code from request
    :return: VerificationCodes or None
    """
    return VerificationCodes.objects.filter(code=code).first()


def get_verification_code_by_email_or_none(email: str) -> VerificationCodes | None:
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


