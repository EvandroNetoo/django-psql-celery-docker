from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .active_account import active_account_send_email, generate_url


@receiver(post_save, sender=User)
def active_account_email(
    sender: User,
    instance: User,
    created: bool,
    **kwargs,
):
    if created and not instance.is_active:
        active_url = generate_url(instance)
        print(active_url)
        active_account_send_email.delay(active_url, instance.email)
