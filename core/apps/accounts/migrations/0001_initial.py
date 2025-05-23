# Generated by Django 5.1.6 on 2025-04-25 17:37

import django.db.models.deletion
import utils.validations
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone', models.CharField(max_length=11, unique=True, validators=[utils.validations.validate_phone], verbose_name='phone')),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='is staff')),
                ('is_phone_verified', models.BooleanField(default=False, verbose_name='is phone verified')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='last name')),
                ('profile_picture', models.ImageField(default='user/profile/user.png', upload_to='user/profile/', verbose_name='profile picture')),
                ('reviews_count', models.IntegerField(default=0, verbose_name='reviews count')),
                ('orders_count', models.IntegerField(default=0, verbose_name='orders count')),
                ('temporary_email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='temporary email')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(verbose_name='address')),
                ('city', models.CharField(max_length=100, verbose_name='city')),
                ('state', models.CharField(max_length=100, verbose_name='state')),
                ('postal_code', models.CharField(max_length=10, unique=True, validators=[utils.validations.custom_postal_code_validator], verbose_name='postal code')),
                ('recipient_phone', models.CharField(max_length=15, verbose_name='recipient phone')),
                ('recipient_name', models.CharField(max_length=100, verbose_name='recipient name')),
                ('is_default', models.BooleanField(default=False, verbose_name='is default')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkouts', to='accounts.profile', verbose_name='user profile')),
            ],
            options={
                'verbose_name': 'Checkout',
                'verbose_name_plural': 'Checkouts',
            },
        ),
    ]
