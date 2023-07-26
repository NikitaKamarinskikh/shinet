from django.db import models
from django.utils.translation import gettext_lazy as _
from modeltranslation.translator import TranslationOptions, register


class Specializations(models.Model):
    name = models.CharField(verbose_name='Name', max_length=100)
    image = models.ImageField(verbose_name='Image', null=True, blank=True)

    def __str__(self):
        return self.name.__str__()

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'


class Services(models.Model):
    specialization = models.ForeignKey(Specializations, on_delete=models.PROTECT)
    master = models.ForeignKey('users.MasterInfo', on_delete=models.PROTECT, null=True)
    name = models.CharField(verbose_name='Название', max_length=255)
    price = models.PositiveIntegerField(verbose_name='Стоимость')
    duration_in_minutes = models.PositiveIntegerField(verbose_name='Diration in minutes')
    description = models.TextField(verbose_name='Description')
    image = models.ImageField(verbose_name='Image', null=True, blank=True)

    def __str__(self):
        return self.name.__str__()

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'




