"""
Señales de la app users.

Crea automáticamente un perfil cuando se registra un usuario nuevo
y lo guarda cuando se actualiza el usuario.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, User


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, raw=False, **kwargs):
    """Si el usuario es nuevo, crea su perfil si no existe. Si raw=True (fixtures), no hace nada."""
    if raw:
        return
    if created:
        Profile.objects.get_or_create(user=instance)
    elif hasattr(instance, 'profile'):
        instance.profile.save()
