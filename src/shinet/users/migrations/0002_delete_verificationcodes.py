# Generated by Django 4.0 on 2023-07-07 04:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VerificationCodes',
        ),
    ]
