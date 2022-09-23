
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import UserSettings


@receiver(post_save, sender=get_user_model())
def user_addons(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.get_or_create(user=instance)