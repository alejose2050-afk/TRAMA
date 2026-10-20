"""Configuración de la app users."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Usuarios'

    def ready(self):
        """Importa las señales cuando la app está lista."""
        import users.signals  # noqa: F401
