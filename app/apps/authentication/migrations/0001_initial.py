# Generated by Django 4.2.7 on 2023-11-13 23:02

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'password',
                    models.CharField(max_length=128, verbose_name='password'),
                ),
                (
                    'last_login',
                    models.DateTimeField(blank=True, null=True, verbose_name='last login'),
                ),
                (
                    'is_superuser',
                    models.BooleanField(
                        default=False,
                        help_text='Designates that this user has all permissions without explicitly assigning them.',
                        verbose_name='superuser status',
                    ),
                ),
                (
                    'username',
                    models.CharField(max_length=150, unique=True, verbose_name='username'),
                ),
                (
                    'email',
                    models.EmailField(
                        max_length=254,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                inverse_match=True,
                                message='Do not use spaces in the username',
                                regex='\\s',
                            )
                        ],
                        verbose_name='email address',
                    ),
                ),
                (
                    'first_name',
                    models.CharField(
                        max_length=32,
                        validators=[
                            django.core.validators.RegexValidator(
                                inverse_match=True,
                                message='Do not use spaces in the username',
                                regex='\\s',
                            )
                        ],
                        verbose_name='first name',
                    ),
                ),
                (
                    'last_name',
                    models.CharField(
                        max_length=32,
                        validators=[
                            django.core.validators.RegexValidator(
                                inverse_match=True,
                                message='Do not use spaces in the username',
                                regex='\\s',
                            )
                        ],
                        verbose_name='last name',
                    ),
                ),
                (
                    'created_at',
                    models.DateField(default=django.utils.timezone.now),
                ),
                (
                    'groups',
                    models.ManyToManyField(
                        blank=True,
                        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                        related_name='user_set',
                        related_query_name='user',
                        to='auth.group',
                        verbose_name='groups',
                    ),
                ),
                (
                    'user_permissions',
                    models.ManyToManyField(
                        blank=True,
                        help_text='Specific permissions for this user.',
                        related_name='user_set',
                        related_query_name='user',
                        to='auth.permission',
                        verbose_name='user permissions',
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
