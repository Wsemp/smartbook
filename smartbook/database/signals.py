from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Level, UnlockedLevel


@receiver(post_save, sender=User)
def unlock_first_level(sender, instance, created, **kwargs):
    if created:
        first_level = Level.objects.order_by('id').first()

        if first_level:
            UnlockedLevel.objects.create(
                user=instance,
                level=first_level
            )
