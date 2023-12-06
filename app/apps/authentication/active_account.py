from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from authentication.models import User

from celery import shared_task


def generate_url(user: User):
    protocol = 'http' if settings.DEBUG else 'https'
    domain = settings.DOMAIN
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    return f'{protocol}://{domain}{reverse("active_account", kwargs={"uidb64": uidb64, "token": token})}'


@shared_task
def active_account_send_email(active_url: str, user_email: str) -> None:
    subject = 'Ative sua conta!!!'
    html_content = render_to_string('mails/active_account.html', {'active_url': active_url})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject,
        text_content,
        to=[user_email],
    )
    email.attach_alternative(html_content, 'text/html')
    email.send()
