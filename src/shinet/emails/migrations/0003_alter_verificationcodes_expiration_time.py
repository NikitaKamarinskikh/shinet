# Generated by Django 4.0 on 2023-03-26 05:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_verificationcodes_expiration_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcodes',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 26, 5, 45, 29, 430681, tzinfo=utc), editable=False, verbose_name='Время истечения'),
        ),
    ]
