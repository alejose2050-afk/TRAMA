"""
Configuración principal de Django para TRAMA.

Lee las credenciales y ajustes sensibles desde variables de entorno
definidas en compose.yaml y el archivo .env local.
"""

import os
from pathlib import Path

# Ruta base del proyecto (directorio que contiene manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent


# --- Seguridad ---

# La clave secreta se lee del entorno. Si no existe, se usa un valor
# por defecto SOLO válido para desarrollo local.
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-clave-solo-para-desarrollo-local'
)

# DEBUG se activa si la variable de entorno DEBUG vale '1'.
# En producción esta variable no debe definirse o debe valer '0'.
DEBUG = os.environ.get('DEBUG', '0') == '1'

# Hosts permitidos para recibir peticiones.
# En desarrollo Docker usa localhost; en producción se deben listar
# los dominios reales.
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# --- Aplicaciones instaladas ---

INSTALLED_APPS = [
    # Apps propias de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Librerías de terceros
    'rest_framework',
    'corsheaders',

    # Apps del proyecto (se agregarán conforme se creen)
    # 'users',
]


# --- Middleware ---

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# --- URLs y plantillas ---

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# --- Base de datos ---
# Se conecta al servicio PostgreSQL definido en compose.yaml.
# Las credenciales se leen de las variables de entorno del contenedor.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'trama'),
        'USER': os.environ.get('DB_USER', 'trama_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


# --- Modelo de usuario personalizado ---
# Se debe definir ANTES de ejecutar la primera migración.
# La app 'users' se creará en el siguiente paso.

# AUTH_USER_MODEL = 'users.User'


# --- Validación de contraseñas ---

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- Internacionalización ---

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Caracas'
USE_I18N = True
USE_TZ = True


# --- Archivos estáticos ---

STATIC_URL = 'static/'


# --- Configuración de claves primarias ---

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- CORS ---
# En desarrollo se permite el origen del frontend local.
# En producción se deben listar únicamente los dominios autorizados.

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]


# --- Django REST Framework ---

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
