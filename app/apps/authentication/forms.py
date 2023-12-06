from django import forms
from django.contrib.auth import forms as auth_forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from authentication.validators import *
from django.utils.translation import gettext_lazy as _
import re


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(),
        validators=[
            special_characters,
            uppercase_letters,
            lowercase_letters,
            number_validator,
            no_whitespaces,
            min_length_6_validator,
        ],
    )

    password2 = forms.CharField(
        label=_('Confirm password'),
        widget=forms.PasswordInput(),
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', _('Passwords do not match.'))

        return cleaned_data


class AdminChangePassowordForm(forms.Form):
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(),
        validators=[
            special_characters,
            uppercase_letters,
            lowercase_letters,
            number_validator,
            no_whitespaces,
            min_length_6_validator,
        ],
    )

    password2 = forms.CharField(
        label=_('Confirm password'),
        widget=forms.PasswordInput(),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', _('Passwords do not match.'))

        return cleaned_data

    def save(self, commit=True):
        password = self.cleaned_data['password1']
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class UserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm):
        model = User
        fields = '__all__'
