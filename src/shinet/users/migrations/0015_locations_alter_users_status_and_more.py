# Generated by Django 4.0 on 2023-04-07 04:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_users_status_alter_verificationcodes_expiration_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255, verbose_name='Город')),
                ('district', models.CharField(max_length=255, verbose_name='Район')),
                ('street', models.CharField(max_length=255, verbose_name='Улица')),
                ('house', models.CharField(max_length=255, verbose_name='Дом')),
                ('office', models.CharField(blank=True, max_length=255, null=True, verbose_name='Офис')),
                ('floor', models.CharField(max_length=255, verbose_name='Этаж')),
                ('extra_info', models.TextField(blank=True, null=True, verbose_name='Дополнительная информация')),
            ],
        ),
        migrations.AlterField(
            model_name='users',
            name='status',
            field=models.CharField(default='Active 🟢', max_length=100, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='verificationcodes',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 7, 4, 33, 36, 922838, tzinfo=utc), editable=False, verbose_name='Время истечения'),
        ),
    ]
