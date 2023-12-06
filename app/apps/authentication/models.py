from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .validators import no_whitespaces

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        blank=False,
        validators=[no_whitespaces],
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
    )
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
    )

    date_joined = models.DateField(
        _('date joined'),
        default=timezone.now,
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['email', 'password']

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self) -> str:
        return f'{self.email} | {self.username}'
