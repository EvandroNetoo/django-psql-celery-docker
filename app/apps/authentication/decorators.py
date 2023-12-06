from typing import Callable
from django.http import HttpRequest
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.utils.translation import gettext_lazy as _


def not_authenticated(redirect_url: str = '/'):
    def _decorator(view_func: Callable):
        def _wrapper(request: HttpRequest, *args, **kwargs):

            if not request.user.is_authenticated:
                return view_func(request, *args, **kwargs)

            messages.add_message(
                request,
                constants.WARNING,
                _('To access this page you must not be logged in.'),
            )
            return redirect(redirect_url)

        return _wrapper

    return _decorator


def authenticated(redirect_url: str = '/'):
    def _decorator(view_func: Callable):
        def _wrapper(request: HttpRequest, *args, **kwargs):

            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)

            messages.add_message(
                request,
                constants.WARNING,
                _('To access this page you must be logged in.'),
            )
            return redirect(redirect_url)

        return _wrapper

    return _decorator
