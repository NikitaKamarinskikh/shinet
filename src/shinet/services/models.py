from django.db import models


class Specializations(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    image = models.ImageField(verbose_name='Фото', null=True, blank=True)

    def __str__(self):
        return self.name.__str__()

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'


class Services(models.Model):
    specialization = models.OneToOneField(Specializations, on_delete=models.PROTECT, primary_key=True)
    master = models.OneToOneField('users.MasterInfo', on_delete=models.PROTECT, null=True)
    name = models.CharField(verbose_name='Название', max_length=255)
    price = models.PositiveIntegerField(verbose_name='Стоимость')

    def __str__(self):
        return self.name.__str__()

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class ServiceImages(models.Model):
    service = models.ForeignKey(Services, verbose_name='Услуга', on_delete=models.PROTECT)
    image = models.ImageField(verbose_name='Фото')

    class Meta:
        verbose_name = 'Фото услуги'
        verbose_name_plural = 'Фото услуг'



