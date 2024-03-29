# Generated by Django 4.0 on 2023-06-28 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_alter_services_image_alter_services_master'),
        ('users', '0001_initial'),
        ('slots', '0005_alter_bookings_client_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnregisteredClientsBookings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateTimeField(verbose_name='Start datetime')),
                ('end_datetime', models.DateTimeField(verbose_name='End datetime')),
                ('client_comment', models.TextField(blank=True, null=True, verbose_name='Client comment')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.unregisteredclients', verbose_name='Client')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='services.services', verbose_name='Service')),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='unregistered_clients_bookings', to='slots.slots', verbose_name='Slot')),
            ],
            options={
                'verbose_name': 'Unregistered clients booking',
                'verbose_name_plural': 'Inregistered clients bookings',
            },
        ),
    ]
