from typing import List, Optional

from . import models


def get_user_phone_numbers(user_id: int) -> List[str]:
    """

    """
    return list(models.UsersPhonesNumbers.objects.values_list('phone_number', flat=True).filter(user_id=user_id))


def get_notification_tokens_by_user_id(user_id: int) -> List[models.NotificationTokens]:
    """

    """
    return list(models.NotificationTokens.objects.filter(user_id=user_id))


def get_notification_token_by_user_id_and_token_or_none(user_id: int, token: str) -> Optional[models.NotificationTokens]:
    """

    """
    return models.NotificationTokens.objects.filter(user_id=user_id, token=token).first()


def create_notification_token_if_not_exists(user_id: int, token: str) -> models.NotificationTokens:
    """

    """
    current_token = get_notification_token_by_user_id_and_token_or_none(user_id, token)
    if current_token is None:
        current_token = models.NotificationTokens.objects.create(user_id=user_id, token=token)
    return current_token


def swap_user_notification_status(user_id: int) -> bool:
    """

    """
    user = models.Users.objects.get(pk=user_id)
    settings = user.settings
    if settings.notification_status:
        settings.notification_status = False
        settings.save()
        return False
    settings.notification_status = True
    settings.save()
    return True




