"""
Modelos de usuario y perfil para TRAMA.

User: modelo personalizado que extiende AbstractUser.
    - Usa el correo electrónico como campo de login.
    - Incluye un campo de rol con cuatro opciones fijas.

Profile: información personal del usuario.
    - Se crea automáticamente al registrar un usuario (ver signals.py).
    - Separado del modelo User para mantener la autenticación
      independiente de los datos de perfil.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """Modelo de usuario personalizado para TRAMA."""

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        MANAGER = 'manager', 'Gestor'
        USER = 'user', 'Usuario'
        VISITOR = 'visitor', 'Visitante'

    email = models.EmailField('correo electrónico', unique=True)
    role = models.CharField(
        'rol',
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )

    # El login se realiza con el correo electrónico
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.get_full_name()} ({self.get_role_display()})'


class Profile(models.Model):
    """Información personal asociada a un usuario."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='usuario',
    )
    phone = models.CharField('teléfono', max_length=20, blank=True)
    department = models.CharField('departamento', max_length=150, blank=True)
    bio = models.TextField('biografía', blank=True)

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'

    def __str__(self):
        return f'Perfil de {self.user.get_full_name()}'
