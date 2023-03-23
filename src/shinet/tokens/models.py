from django.db import models
from users.models import Users


class RefreshTokens(models.Model):
    user = models.OneToOneField(Users, verbose_name='Пользователь',
                                on_delete=models.CASCADE)
    token = models.CharField(verbose_name='Токен', max_length=255)

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'
