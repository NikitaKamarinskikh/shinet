# Generated by Django 4.0 on 2023-04-08 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_alter_services_name_serviceimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='specializations',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Фото'),
        ),
    ]
