"""
Señales de la app users.

Crea automáticamente un perfil cuando se registra un usuario nuevo
y lo guarda cuando se actualiza el usuario.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, User


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """Si el usuario es nuevo, crea su perfil. Si ya existe, lo guarda."""
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
