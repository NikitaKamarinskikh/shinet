from datetime import datetime, timedelta, timezone

from django.db import models


DEFAULT_VERIFICATION_CODE_LIFETIME_IN_MINUTES = 5


def get_code_expiration_time() -> datetime:
    """Calculate code lifetime (starts from current time in utc)
        and return timestamp
    :return: code expiration time
    :rtype: datetime.datetime
    """
    current_utc_time = datetime.now(timezone.utc)
    code_expiration_time = current_utc_time + timedelta(minutes=DEFAULT_VERIFICATION_CODE_LIFETIME_IN_MINUTES)
    return code_expiration_time


class VerificationCodes(models.Model):
    email = models.EmailField(verbose_name='Email', unique=True)
    code = models.PositiveIntegerField(verbose_name='Код', unique=True)
    expiration_time = models.DateTimeField(verbose_name='Время истечения',
                                           default=get_code_expiration_time, editable=False)

    class Meta:
        verbose_name = 'Код для проверки'
        verbose_name_plural = 'Коды для проверки'

    def __str__(self) -> str:
        return f'{self.email} {self.code}'


class VerificationTokens(models.Model):
    email = models.EmailField(verbose_name='Email', unique=True)
    token = models.CharField(verbose_name='Token', max_length=500, unique=True)

    class Meta:
        verbose_name = 'Токен проверки'
        verbose_name_plural = 'Токены для проверки'

    def __str__(self) -> str:
        return f'{self.email} {self.token}'



