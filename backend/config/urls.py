"""
Configuración central de URLs para TRAMA.

Rutas principales:
- '': Página de inicio / catálogo y presentación del sistema.
- 'usuarios/': Módulo de autenticación, registro y perfiles.
- 'admin/': Panel de administración de Django para gestión de modelos.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from users.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('usuarios/', include('users.urls', namespace='users')),
]

# En modo de desarrollo, permite servir archivos estáticos y multimedia
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
