"""
Manager personalizado para el modelo User.

Sobreescribe la creación de usuarios para que el campo principal
de identificación sea el correo electrónico en lugar del username.
"""

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Manager que usa el correo electrónico como identificador
    principal para la creación de usuarios.
    """

    def create_user(self, email, username, password=None, **extra_fields):
        """Crea y guarda un usuario con email, username y contraseña."""
        if not email:
            raise ValueError('El correo electrónico es obligatorio.')
        if not username:
            raise ValueError('El nombre de usuario es obligatorio.')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """Crea un superusuario con rol de administrador."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Un superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Un superusuario debe tener is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)
