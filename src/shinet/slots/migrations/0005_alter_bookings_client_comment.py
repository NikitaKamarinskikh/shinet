# Generated by Django 4.0 on 2023-06-26 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slots', '0004_bookings_client_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='client_comment',
            field=models.TextField(blank=True, null=True, verbose_name='Client comment'),
        ),
    ]
