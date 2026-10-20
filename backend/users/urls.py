"""
Enrutamiento de URLs para el módulo de usuarios y autenticación de TRAMA.
"""

from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('registro/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.profile_view, name='profile'),
]
