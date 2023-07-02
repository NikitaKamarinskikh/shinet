# Generated by Django 4.0 on 2023-04-27 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefreshTokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255, verbose_name='Токен')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.users', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Токен',
                'verbose_name_plural': 'Токены',
            },
        ),
    ]
