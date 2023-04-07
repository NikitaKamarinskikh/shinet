from datetime import datetime, timedelta, timezone
import uuid
from django.db import models
from services.models import Specializations
from subscriptions.models import ActiveSubscriptions
from subscriptions.services import get_trial_subscription
from .settings import UsersRoles, UsersStatuses


DEFAULT_VERIFICATION_CODE_LIFETIME_IN_MINUTES = 5


class Users(models.Model):
    role = models.CharField(verbose_name='Роль', max_length=30)
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    email = models.EmailField(verbose_name='Почта', unique=True)
    password = models.CharField(verbose_name='Пароль', max_length=255)
    sex = models.CharField(verbose_name='Пол', max_length=30)
    created_at = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)
    settings = models.OneToOneField('UserSettings', on_delete=models.CASCADE, null=True)
    master_info = models.OneToOneField('MasterInfo', on_delete=models.CASCADE, null=True, blank=True)
    profile_image = models.ImageField(verbose_name='Фото профиля', null=True, blank=True)
    status = models.CharField(verbose_name='Статус', max_length=100, default=UsersStatuses.ACTIVE.value)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        settings = UserSettings.objects.create()
        self.settings = settings
        if self.role == UsersRoles.MASTER.value:
            trial_subscription = get_trial_subscription()
            active_subscription = ActiveSubscriptions.objects.create(
                subscription=trial_subscription,
                start=datetime.now(timezone.utc),
                end=datetime.now(timezone.utc),
            )
            master_info = MasterInfo.objects.create(
                active_subscription=active_subscription
            )
            self.master_info = master_info
        super().save()

    def delete(self, *args, **kwargs):
        self.settings.delete()
        self.master_info.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class MasterInfo(models.Model):
    location = models.CharField(verbose_name='Местоположение', max_length=100, null=True,
                                blank=True, default='Unknown')
    rating = models.PositiveIntegerField(verbose_name='Рейтинг', default=0)
    specializations = models.ManyToManyField(Specializations, blank=True, verbose_name='Специализации')
    active_subscription = models.OneToOneField(ActiveSubscriptions, on_delete=models.CASCADE,
                                               verbose_name='Активная подписка')
    uuid = models.PositiveIntegerField(verbose_name='UUID', default=0, unique=True)

    def __str__(self) -> str:
        return self.uuid.__str__()

    class Meta:
        verbose_name = 'Информация мастера'
        verbose_name_plural = 'Информации мастеров'


class Locations(models.Model):
    city = models.CharField(verbose_name='Город', max_length=255)
    district = models.CharField(verbose_name='Район', max_length=255)
    street = models.CharField(verbose_name='Улица', max_length=255)
    house = models.CharField(verbose_name='Дом', max_length=255)
    office = models.CharField(verbose_name='Офис', max_length=255, null=True, blank=True)
    floor = models.CharField(verbose_name='Этаж', max_length=255)
    extra_info = models.TextField(verbose_name='Дополнительная информация', null=True, blank=True)

    def __str__(self):
        return f'{self.city} {self.district} {self.street}'

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'


class UserSettings(models.Model):
    color_theme = models.CharField(verbose_name='Цветовая тема', max_length=255, default='LIGHT')

    class Meta:
        verbose_name = 'Настройки пользователя'
        verbose_name_plural = 'Настройки пользователей'


class UsersPhonesNumbers(models.Model):
    user = models.ForeignKey(Users, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=255)

    class Meta:
        verbose_name = 'Номер телефона пользователя'
        verbose_name_plural = 'Номера телефонов пользователей'


class UnregisteredClients(models.Model):
    master = models.ForeignKey(MasterInfo, verbose_name='Мастер', on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Незарегистрированный клиент'
        verbose_name_plural = 'Незарегистрированные клиенты'


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
                                           default=get_code_expiration_time(), editable=False)

    def __str__(self) -> str:
        return f'{self.email} {self.code}'

    class Meta:
        verbose_name = 'Код для проверки'
        verbose_name_plural = 'Коды для проверки'


