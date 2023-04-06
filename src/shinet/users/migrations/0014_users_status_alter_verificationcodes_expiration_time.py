# Generated by Django 4.0 on 2023-04-06 14:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import users.settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_verificationcodes_expiration_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='status',
            field=models.CharField(default=users.settings.UsersStatuses['ACTIVE'], max_length=100, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='verificationcodes',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 6, 15, 1, 18, 464370, tzinfo=utc), editable=False, verbose_name='Время истечения'),
        ),
    ]
