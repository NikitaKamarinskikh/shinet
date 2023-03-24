from django.db import models


class VerificationCodes(models.Model):
    email = models.EmailField(verbose_name='Email', unique=True)
    code = models.PositiveIntegerField(verbose_name='Код', unique=True)

    def __str__(self) -> str:
        return f'{self.email} {self.code}'

    class Meta:
        verbose_name = 'Код для проверки'
        verbose_name_plural = 'Коды для проверки'

