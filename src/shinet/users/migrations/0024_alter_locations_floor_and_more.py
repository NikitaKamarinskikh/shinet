# Generated by Django 4.0 on 2023-04-17 12:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_alter_verificationcodes_expiration_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locations',
            name='floor',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Этаж'),
        ),
        migrations.AlterField(
            model_name='verificationcodes',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 17, 12, 40, 58, 182628, tzinfo=utc), editable=False, verbose_name='Время истечения'),
        ),
    ]
