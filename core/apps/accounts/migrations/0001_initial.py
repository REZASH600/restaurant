# Generated by Django 5.1.6 on 2025-03-11 07:06

import apps.accounts.validations
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone', models.CharField(max_length=11, unique=True, validators=[apps.accounts.validations.validate_phone], verbose_name='phone')),
                ('username', models.CharField(max_length=255, verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_admin', models.BooleanField(default=False, verbose_name='is admin')),
                ('is_staff', models.BooleanField(default=False, verbose_name='is staff')),
                ('is_phone_verified', models.BooleanField(default=False, verbose_name='is phone verified')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
