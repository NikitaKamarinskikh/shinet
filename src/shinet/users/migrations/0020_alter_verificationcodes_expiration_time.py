# Generated by Django 4.0 on 2023-04-08 06:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_masterinfo_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcodes',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 8, 6, 51, 19, 454327, tzinfo=utc), editable=False, verbose_name='Время истечения'),
        ),
    ]
