# Generated by Django 4.0 on 2023-04-21 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('subscriptions', '0004_rename_price_subscriptions_price_without_discount'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ActiveSubscriptions',
            new_name='MastersSubscriptions',
        ),
    ]