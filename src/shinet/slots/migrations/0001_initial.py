# Generated by Django 4.0 on 2023-04-29 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('services', '0004_alter_services_image_alter_services_master'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateTimeField(verbose_name='Start datetime')),
                ('end_datetime', models.DateTimeField(verbose_name='End datetime')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.masterinfo', verbose_name='Master')),
            ],
            options={
                'verbose_name': 'Slot',
                'verbose_name_plural': 'Slots',
            },
        ),
        migrations.CreateModel(
            name='ServiceRecords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateTimeField(verbose_name='Start datetime')),
                ('end_datetime', models.DateTimeField(verbose_name='End datetime')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.users', verbose_name='Client')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='services.services', verbose_name='Service')),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='slots.slots', verbose_name='Slot')),
            ],
            options={
                'verbose_name': 'Service record',
                'verbose_name_plural': 'Service records',
            },
        ),
    ]
