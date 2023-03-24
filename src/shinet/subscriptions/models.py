from django.db import models
from .settings import SubscriptionTypes


class Subscriptions(models.Model):
    price = models.PositiveIntegerField(verbose_name='Стоимость')
    type = models.CharField(verbose_name='Тип', max_length=255,
                            choices=SubscriptionTypes.choices(), unique=True)

    def __str__(self):
        return self.type.__str__()

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class ActiveSubscriptions(models.Model):
    subscription = models.ForeignKey(Subscriptions, on_delete=models.PROTECT, verbose_name='Подписка')
    start = models.DateTimeField(verbose_name='Дата начала')
    end = models.DateTimeField(verbose_name='Дата окончания')

    class Meta:
        verbose_name = 'Активная подписка'
        verbose_name_plural = 'Активные подписки'
