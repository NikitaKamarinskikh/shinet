from django.db import models


class Users(models.Model):
    role = models.CharField(verbose_name='Роль', max_length=30)
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    email = models.EmailField(verbose_name='Почта')
    password = models.CharField(verbose_name='Пароль', max_length=255)
    sex = models.CharField(verbose_name='Пол', max_length=30)
    created_at = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)
    settings = models.OneToOneField('UserSettings', on_delete=models.PROTECT,
                                    null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserSettings(models.Model):
    color_theme = models.CharField(verbose_name='Цветовая тема', max_length=255)

    class Meta:
        verbose_name = 'Настройки пользователя'
        verbose_name_plural = 'Настройки пользователей'

