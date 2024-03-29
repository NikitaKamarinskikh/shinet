# Generated by Django 4.0 on 2023-04-27 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('services', '0003_services_description_services_duration_in_minutes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='services',
            name='master',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='users.masterinfo'),
        ),
    ]
