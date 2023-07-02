# Generated by Django 4.0 on 2023-05-04 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('services', '0004_alter_services_image_alter_services_master'),
        ('slots', '0002_delete_servicerecords'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateTimeField(verbose_name='Start datetime')),
                ('end_datetime', models.DateTimeField(verbose_name='End datetime')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.users', verbose_name='Client')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='services.services', verbose_name='Service')),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bookings', to='slots.slots', verbose_name='Slot')),
            ],
            options={
                'verbose_name': 'Booking',
                'verbose_name_plural': 'Bookings',
            },
        ),
    ]