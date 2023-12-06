from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
    authenticate,
    get_user_model,
)
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.messages import constants
from django.utils.translation import gettext_lazy as _

from authentication.active_account import (
    active_account_send_email,
    generate_url,
)
from authentication.decorators import not_authenticated, authenticated
from authentication.forms import UserCreationForm


@not_authenticated(redirect_url='home')
def register(request: HttpRequest) -> HttpResponse:
    match request.method:
        case 'GET':
            return render(request, 'register.html')

        case 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                try:
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password1'])
                    user.is_active = False
                    user.save()
                    messages.add_message(
                        request,
                        constants.SUCCESS,
                        'An email was sent with the account activation link.',
                    )
                    return redirect('login')

                except Exception as e:
                    print(e)
                    messages.add_message(request, constants.ERROR, _('A server error occurred.'))
            return render(request, 'register.html', {'form': form})


@not_authenticated(redirect_url='home')
def active_account(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    match request.method:
        case 'GET':
            uid = force_str(urlsafe_base64_decode(uidb64))
            user_model = get_user_model()
            user = user_model.objects.filter(pk=uid)

            if (user := user.first()) and default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                auth_login(request, user)
                messages.add_message(
                    request,
                    constants.SUCCESS,
                    _('User activated successfully.'),
                )
                return redirect('home')

            messages.add_message(request, constants.ERROR, _('Invalid account activation link.'))
            return redirect('login')


@not_authenticated(redirect_url='home')
def login(request: HttpRequest) -> HttpResponse:
    match request.method:
        case 'GET':
            return render(request, 'login.html')

        case 'POST':
            username_email = request.POST.get('username_email')
            password = request.POST.get('password')

            user = authenticate(username=username_email, password=password)
            if not user:
                messages.add_message(request, constants.ERROR, _('Invalid credentials.'))
                return redirect('login')

            if not user.is_active:
                active_url = generate_url(user)
                print(active_url)
                active_account_send_email.delay(active_url, user.email)

                messages.add_message(
                    request,
                    constants.ERROR,
                    _('User not activated, an email was sent with the activation link.'),
                )
                return redirect('login')

            auth_login(request, user)
            return redirect('home')


@authenticated(redirect_url='login')
def logout(request: HttpRequest) -> HttpResponse:
    match request.method:
        case 'GET':
            auth_logout(request)
            messages.add_message(request, constants.SUCCESS, _('Successfully logged out.'))
            return redirect('login')


@authenticated(redirect_url='login')
def home(request: HttpRequest) -> HttpResponse:
    match request.method:
        case 'GET':
            return render(request, 'partials/messages.html')

        case 'POST':
            return
