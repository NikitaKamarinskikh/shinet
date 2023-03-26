from datetime import datetime, timedelta, timezone
from django.db import models


DEFAULT_CODE_LIFETIME_IN_MINUTES = 5


def get_code_expiration_time() -> datetime:
    """Calculate code lifetime and return timestamp
    :return: code expiration time
    :rtype: datetime.datetime
    """
    current_utc_time = datetime.now(timezone.utc)
    code_expiration_time = current_utc_time + timedelta(minutes=DEFAULT_CODE_LIFETIME_IN_MINUTES)
    return code_expiration_time


class VerificationCodes(models.Model):
    email = models.EmailField(verbose_name='Email', unique=True)
    code = models.PositiveIntegerField(verbose_name='Код', unique=True)
    expiration_time = models.DateTimeField(verbose_name='Время истечения',
                                           default=get_code_expiration_time(), editable=False)

    def __str__(self) -> str:
        return f'{self.email} {self.code}'

    class Meta:
        verbose_name = 'Код для проверки'
        verbose_name_plural = 'Коды для проверки'

