# Generated by Django 4.0 on 2023-03-22 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_users_email_alter_users_master_info'),
        ('tokens', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refreshtokens',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.users', unique=True, verbose_name='Пользователь'),
        ),
    ]
