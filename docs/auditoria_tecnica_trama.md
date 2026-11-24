# AUDITORÍA TÉCNICA INTEGRAL DEL PROYECTO TRAMA
**Plataforma Integral de Gestión y Articulación de Recursos Universitarios**

---

| Metadato | Detalle de Auditoría |
| :--- | :--- |
| **Fecha de Auditoría** | Noviembre 2026 |
| **Repositorio Evaluado** | `trama-platform` (`main`) |
| **Tipo de Evaluación** | Inspección Estática de Código Fuente, Configuración de Contenedores y Dependencias |
| **Rol Evaluador** | Arquitecto de Software & Tutor Académico de Ingeniería Informática |
| **Objetivo** | Verificación técnica real del estado de implementación para defensa académica |

---

## 1. Contexto y Objetivos del Proyecto

El proyecto **TRAMA** se concibe como una plataforma orientada a la comunidad universitaria para la articulación, préstamo y control de recursos tecnológicos, espacios físicos y apoyo a actividades académicas (clases prácticas, talleres de subproyectos y defensas de proyectos de grado).

El sistema formaliza cuatro roles de usuario:
1. **Administrador:** Auditoría global, gestión de cuentas y control relacional mediante panel de base de datos.
2. **Gestor / Docente:** Supervisión y aprobación de solicitudes de recursos asignados a su departamento o área.
3. **Usuario / Estudiante:** Consulta de disponibilidad y solicitud de equipos/espacios para sus subproyectos.
4. **Visitante:** Consulta pública del catálogo institucional sin sesión iniciada.

---

## 2. Inspección de la Estructura Real del Repositorio

A partir de la exploración del sistema de archivos, se comprobó que el repositorio está organizado en dos componentes desacoplados a nivel de código (`backend/` y `frontend/`), orquestados mediante archivos de infraestructura en la raíz.

### Árbol de Directorios Comprobado

```text
trama-platform/
├── .dockerignore                   # Exclusiones de contexto para el daemon de Docker
├── .env.example                    # Plantilla de variables de entorno (sin credenciales sensibles)
├── .gitignore                      # Exclusiones de Git (entornos virtuales, cachés, secretos)
├── compose.yaml                    # Especificación de servicios Docker Compose (backend y db)
├── README.md                       # Documentación general y memoria del proyecto
├── docs/                           # Documentación técnica e infografías
│   ├── infografia_modelo_v.jpg     # Infografía del Modelo en V aplicado
│   └── auditoria_tecnica_trama.md  # Informe formal de auditoría técnica
├── backend/                        # Núcleo del Backend en Python / Django
│   ├── Dockerfile                  # Imagen base (python:3.13-slim) y dependencias
│   ├── manage.py                   # CLI administrativo de Django
│   ├── requirements.txt            # Dependencias Python del backend
│   ├── config/                     # Paquete de configuración raíz de Django
│   │   ├── asgi.py                 # Punto de entrada para servidores asíncronos ASGI
│   │   ├── settings.py             # Configuración central (BD, apps, middleware, CORS, DRF)
│   │   ├── urls.py                 # Enrutador principal de URLs y personalización del Admin
│   │   └── wsgi.py                 # Punto de entrada para servidores WSGI
│   ├── static/                     # Archivos estáticos institucionales
│   │   ├── css/
│   │   │   └── trama.css           # Hoja de estilos con variables CSS y diseño institucional
│   │   └── img/
│   │       ├── infografia_modelo_v.jpg
│   │       └── trama_logo.png      # Identidad gráfica del sistema
│   ├── templates/                  # Sistema de plantillas HTML (Django Templates)
│   │   ├── base.html               # Plantilla maestra (Layout con navbar, mensajes y footer)
│   │   ├── home.html               # Despachador de dashboards según rol
│   │   ├── roles/                  # Vistas modulares por perfil
│   │   │   ├── dashboard_admin.html
│   │   │   ├── dashboard_manager.html
│   │   │   ├── dashboard_user.html
│   │   │   └── landing_visitor.html
│   │   └── users/                  # Formularios de autenticación
│   │       ├── login.html
│   │       ├── profile.html
│   │       └── register.html
│   └── users/                      # Aplicación Django 'users' (Autenticación y perfiles)
│       ├── admin.py                # Personalización del modelo User y Profile en Django Admin
│       ├── apps.py                 # Configuración de la app y conexión de signals
│       ├── forms.py                # Formularios validados (Registro, Login, Perfil)
│       ├── managers.py             # UserManager personalizado (login mediante email)
│       ├── models.py               # Modelos User (AbstractUser) y Profile (OneToOne)
│       ├── signals.py              # Señal post_save para sincronización de perfil
│       ├── urls.py                 # Rutas de la app (/usuarios/registro, login, logout, perfil)
│       ├── views.py                # Lógica de controladores y vistas adaptativas
│       ├── fixtures/
│       │   └── initial_users.json  # Datos de prueba para carga inicial (loaddata)
│       └── migrations/
│           ├── 0001_initial.py     # Migración inicial de tablas User y Profile
│           └── __init__.py
└── frontend/                       # Proyecto independiente con Vite.js y React 19
    ├── .dockerignore
    ├── .gitignore
    ├── .oxlintrc.json              # Configuración del linter Oxlint
    ├── Dockerfile                  # Imagen base (node:22-alpine)
    ├── index.html                  # Contenedor HTML raíz de la SPA
    ├── package.json                # Dependencias Node.js (React 19, Vite 8)
    ├── package-lock.json           # Árbol exacto de dependencias de Node
    ├── vite.config.js              # Configuración de empaquetado y servidor Vite
    ├── public/                     # Estáticos públicos (favicons, logos)
    └── src/                        # Código fuente React
        ├── App.css                 # Estilos específicos del componente React
        ├── App.jsx                 # Componente principal con verificación de conexión
        ├── index.css               # Estilos globales de React
        └── main.jsx                # Punto de montaje ReactDOM en `#root`
```

---

## 3. Identificación y Realidad de la Arquitectura de Software

```
+-------------------------------------------------------------------------------+
|                      ESTADO ARQUITECTÓNICO REAL EN TRAMA                      |
+-------------------------------------------------------------------------------+
|                                                                               |
|  [ NAVEGADOR DEL USUARIO ]                                                    |
|           |                                                                   |
|           | HTTP Request (Puerto 8000)                                        |
|           v                                                                   |
|  +-------------------------------------------------------------------------+  |
|  | CONTENEDOR 'trama-backend' (Django 5.2.11 / Python 3.13)                |  |
|  |                                                                         |  |
|  |   [ config/urls.py ] --> Despacho de rutas                              |  |
|  |          |                                                              |  |
|  |          v                                                              |  |
|  |   [ users/views.py (home_view, login_view, etc.) ] (Controlador/View)   |  |
|  |          |                                                              |  |
|  |          +---> [ users/models.py (User, Profile) ] (Modelo/Model)       |  |
|  |          |                                                              |  |
|  |          v                                                              |  |
|  |   [ templates/*.html ] (Plantilla/Template - SSR)                       |  |
|  +-------------------------------------------------------------------------+  |
|           |                                                                   |
|           | Conexión TCP (Puerto 5432 - Driver psycopg v3)                    |
|           v                                                                   |
|  +-------------------------------------------------------------------------+  |
|  | CONTENEDOR 'trama-db' (PostgreSQL 17)                                   |  |
|  | Volumen persistente: postgres_data                                      |  |
|  +-------------------------------------------------------------------------+  |
|                                                                               |
|  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  |
|  [ REPOSITORIO FRONTEND DESACOPLADO ]                                         |
|  `frontend/` (Vite 8 + React 19)                                              |
|  * Configurado en código, NO activo en compose.yaml ni consumido por Django.  |
|  * Funciona como base para la futura fase de API REST.                        |
+-------------------------------------------------------------------------------+
```

### Arquitecturas Comprobadas:

1. **Arquitectura Monolítica Modular (Backend):**
   - **Comprobación:** Todo el flujo operativo de negocio se resuelve dentro del proyecto Django.
   - **Modularidad:** El backend está diseñado para alojar aplicaciones Django independientes. Actualmente está implementada la app `users`.
   - **Estado:** **IMPLEMENTADO Y VERIFICADO**.

2. **Patrón MVT (Model - View - Template) de Django:**
   - **Model:** `users/models.py` define la estructura relacional (`User`, `Profile`).
   - **View:** `users/views.py` gestiona la lógica de negocio y selección de contextos.
   - **Template:** `templates/base.html`, `templates/home.html` y las plantillas en `templates/roles/`.
   - **Estado:** **IMPLEMENTADO Y VERIFICADO**.

3. **Arquitectura Cliente - Servidor:**
   - **Comprobación:** El cliente (navegador web) emite peticiones HTTP que son atendidas por Django en el socket `0.0.0.0:8000`.
   - **Estado:** **IMPLEMENTADO Y VERIFICADO**.

---

## 4. Auditoría de Cuentas y Credenciales de Prueba

Para la evaluación del sistema, las credenciales han sido formalizadas bajo dominios públicos estandarizados (**Gmail y Hotmail**) con la contraseña unificada **`Trama2026`**:

| Rol del Sistema | Titular de Prueba | Correo Electrónico (Gmail / Hotmail) | Contraseña | Vistas y Capacidades Evaluables |
| :--- | :--- | :--- | :--- | :--- |
| **Administrador** | Carlos Mendoza | `admin@gmail.com` | `Trama2026` | Consola global, métricas de PostgreSQL y acceso al [Django Admin](http://127.0.0.1:8000/admin/). |
| **Gestor / Docente** | Prof. Rafael Barrios | `docente@hotmail.com` | `Trama2026` | Panel de gestión docente, aprobación de solicitudes y control de recursos. |
| **Estudiante** | Mariana Silva | `estudiante@gmail.com` | `Trama2026` | Panel del estudiante, estado de solicitudes personales y proyectos académicos. |
| **Visitante** | *Público General* | *(Sin iniciar sesión)* | N/A | Consulta del catálogo público de recursos y acceso al formulario de login/registro. |

---

## 5. Auditoría de Tecnologías y Versiones Comprobadas

| Tecnología | Categoría | Versión Comprobada | Archivo Fuente | Función Real en el Proyecto |
| :--- | :--- | :--- | :--- | :--- |
| **Python** | Lenguaje Backend | `3.13` (en Dockerfile) / `3.12` | `backend/Dockerfile` (`python:3.13-slim`) | Entorno de ejecución de la lógica del servidor. |
| **Django** | Framework Web | `5.2.11` | `backend/requirements.txt` | Framework de desarrollo rápido: MVT, ORM, autenticación y admin. |
| **Django REST Framework** | Librería API | `>=3.16, <4.0` | `backend/requirements.txt` | Preparación para la capa de servicios REST. |
| **psycopg (v3)** | Driver de BD | `>=3.2, <4.0` | `backend/requirements.txt` | Adaptador moderno de PostgreSQL para Python. |
| **django-cors-headers** | Middleware HTTP | `>=4.7, <5.0` | `backend/requirements.txt` | Manejo de cabeceras CORS para peticiones externas. |
| **PostgreSQL** | Base de Datos | `17` | `compose.yaml` (`postgres:17`) | Sistema de gestión de bases de datos relacional. |
| **Docker & Compose** | Contenedores | Especificación Compose v2 | `compose.yaml` | Orquestación de servicios, volúmenes persistentes y redes. |
| **React** | Biblioteca UI | `^19.3.1` | `frontend/package.json` | Scaffolding de interfaz cliente SPA. |
| **Vite.js** | Bundler Frontend | `^8.3.4` | `frontend/package.json` | Empaquetado rápido y servidor de desarrollo para React. |
| **Git / GitHub** | Control Versiones | Git 2.x | `.git/`, `.gitignore` | Control de versiones distribuido alojado en GitHub (`origin/main`). |

---

## 6. Estado Actual de Implementación de Componentes

| Componente | Estado de Auditoría | Justificación Técnica |
| :--- | :--- | :--- |
| **Contenedor PostgreSQL 17** | **IMPLEMENTADO Y VERIFICADO** | Servicio configurado en Compose, volumen persistente `postgres_data`. |
| **Contenedor Django 5.2 Backend** | **IMPLEMENTADO Y VERIFICADO** | Imagen Dockerfile construida sobre Python 3.13-slim, sirviendo en puerto 8000. |
| **Modelo User Personalizado** | **IMPLEMENTADO Y VERIFICADO** | Hereda de AbstractUser, autentica con email (`admin@gmail.com`, etc.). |
| **Modelo Profile y Señales** | **IMPLEMENTADO Y VERIFICADO** | Relación OneToOne, sincronizado mediante post_save con manejo de cargas raw. |
| **Flujo de Registro y Login** | **IMPLEMENTADO Y VERIFICADO** | Formularios Django validados, sesiones criptográficas y redirección dinámica. |
| **Plantillas Adaptativas por Rol** | **IMPLEMENTADO Y VERIFICADO** | Renderizado condicional en `home.html` para Administrador, Gestor, Estudiante y Visitante. |
| **Django Admin Personalizado** | **IMPLEMENTADO Y VERIFICADO** | Panel adaptado con inlines de perfil, filtros, buscadores y cabecera institucional. |
| **Estilos Institucionales CSS** | **IMPLEMENTADO Y VERIFICADO** | Archivo `trama.css` modular con tipografía Plus Jakarta Sans y paleta corporativa. |
| **Scaffolding Vite.js + React 19** | **CONFIGURADO** | Proyecto presente en `frontend/`, compila de forma aislada, inerte en runtime actual. |
| **Django REST Framework (DRF)** | **CONFIGURADO** | Dependencia instalada y declarada en settings, lista para la Fase 2. |
| **Persistencia de Recursos / Préstamos** | **PLANIFICADO / PARCIAL** | Las interfaces muestran tarjetas y tablas con datos mock en memoria. |
