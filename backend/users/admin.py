"""
Configuración del panel de administración para usuarios y perfiles.

Se personaliza la vista del modelo User para mostrar los campos
relevantes y se incluye el perfil como sección editable dentro
de la misma página del usuario.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Profile, User


class ProfileInline(admin.StackedInline):
    """Muestra el perfil dentro de la página del usuario en Admin."""
    model = Profile
    can_delete = False
    verbose_name = 'perfil'
    verbose_name_plural = 'perfil'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Configuración del modelo User en Django Admin."""

    inlines = [ProfileInline]

    # Columnas visibles en la lista de usuarios
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('last_name', 'first_name')

    # Campos en el formulario de edición de usuario
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name')}),
        ('Rol y permisos', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )

    # Campos en el formulario de creación de usuario nuevo
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )
