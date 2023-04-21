from django.db import models
from users.models import MasterInfo


class Subscriptions(models.Model):
    class Status(models.TextChoices):
        TRIAL = 'TRIAL', 'Trial'
        PRO = 'PRO', 'Pro'

    price_without_discount = models.PositiveIntegerField(verbose_name='Стоимость')
    price_with_discount = models.PositiveIntegerField(verbose_name='Стоимость со скидкой')
    discount_in_percent = models.PositiveIntegerField(verbose_name='Скидка в процентах')
    type = models.CharField(verbose_name='Тип', max_length=255,
                            choices=Status.choices, unique=True)
    image = models.ImageField(verbose_name='Изображение', null=True, blank=True)

    def __str__(self):
        return self.type.__str__()

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class MastersSubscriptions(models.Model):
    class Status(models.TextChoices):
        EXPIRED = 'EX', 'Expired'
        PAID = 'PAID', 'Paid'
        ACTIVE = 'ACT', 'Active'

    master = models.ForeignKey(MasterInfo, verbose_name='Мастер', on_delete=models.PROTECT)
    subscription = models.ForeignKey(Subscriptions, on_delete=models.PROTECT, verbose_name='Подписка')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    status = models.CharField(verbose_name='Статус', max_length=10, choices=Status.choices)

    class Meta:
        verbose_name = 'Подписка мастера'
        verbose_name_plural = 'Подписки мастеров'





