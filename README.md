# TRAMA
## Plataforma Integral de Gestión y Articulación de Recursos Universitarios

> ### 📌 Nota para el Docente / Evaluación Académica
> **Profesor Rafael Barrios:** Aquí se encuentran implementadas y organizadas las condiciones previstas que colocó en el Classroom para el desarrollo del proyecto. Si de alguna manera esta primera fase se aprecia más desarrollada de lo pedido inicialmente, el motivo es porque estoy a punto de quedarme temporalmente sin computadora y quería dejar las cosas lo más adelantadas y estructuradas posible para poder migrarme a mi nuevo dispositivo prontamente. Ya que no tengo una fecha estimada exacta de cuándo me llega la nueva o cuándo me quedo sin mi computadora actual, quise dejar todo lo más adelantado posible para no tener problemas en el futuro con las próximas entregas.

---

## 1. Génesis y Origen de TRAMA

**TRAMA** no surge como una idea aislada, sino como la **unión e integración armónica de tres ideas y vertientes de proyectos diferentes**, todas orientadas a resolver necesidades críticas de los **estudiantes universitarios**:

1. **Organización y Seguimiento de Tareas Estudiantiles:** La necesidad de los estudiantes universitarios de contar con un sistema ágil para la planificación de tareas académicas, asignación de responsabilidades en equipo y control de flujos de trabajo secuenciales.
2. **Administración y Control de Recursos:** La importancia de gestionar y optimizar recursos, presupuestos y activos de apoyo a las actividades universitarias, aportando trazabilidad, disponibilidad de inventario y orden administrativo.
3. **Coordinación de Proyectos y Trabajos de Grado:** La necesidad cotidiana de coordinar defensas de grado, prácticas de campo, subproyectos y disponer a tiempo de recursos tecnológicos y espacios físicos (como video beams, salas de conferencias y laboratorios) sin contratiempos.

La convergencia de estas tres ideas dio nacimiento a **TRAMA**: una plataforma centralizada que articula el préstamo de bienes institucionales, la validación docente y el respaldo integral a las iniciativas académicas de la comunidad universitaria.

---

## 2. Introducción

TRAMA es una plataforma web orientada a facilitar la organización de actividades académicas y la coordinación de recursos entre los miembros de la comunidad universitaria. Su propósito es centralizar la consulta de recursos, la gestión de solicitudes y el seguimiento de préstamos para el desarrollo de proyectos y prácticas estudiantiles.

Para guiar su construcción, se utiliza la **metodología de desarrollo en V**, siguiendo su ciclo estructurado para definir requisitos, arquitectura y diseño modular antes de pasar a la codificación.

---

## 3. Metodología de Desarrollo en V

```
  [1. Requisitos del Sistema]                 [Pruebas de Aceptación]
         \                                            /
      [2. Análisis del Sistema]               [Pruebas de Sistema]
             \                                    /
          [3. Diseño de Arquitectura]     [Pruebas de Integración]
                 \                            /
              [4. Diseño Modular]     [Pruebas Unitarias]
                     \                    /
                      [5. Punto Inflexión]
                               |
                        [6. Codificación]
```

### 3.1. Análisis de Requisitos (*Requirement Gathering*)

En esta etapa se identificaron las necesidades operativas de los estudiantes y el cuerpo docente:

* **Registro, inicio de sesión y perfiles:** Identificación por correo institucional o personal, cédula, teléfono y facultad o departamento académico.
* **Administración de roles y permisos (RBAC):** Separación estricta de privilegios entre Administrador, Gestor, Usuario y Visitante.
* **Catálogo de recursos disponibles:** Inventario clasificado de equipos audiovisuales, laboratorios y espacios para actividades académicas.
* **Coordinación de solicitudes y préstamos:** Solicitud formal de equipos vinculada a proyectos y defensas de grado, con control de disponibilidad y aprobación docente.
* **Seguimiento del estado de solicitudes:** Trazabilidad en tiempo real (*Pendiente*, *Aprobado*, *Rechazado*, *Finalizado*).
* **Consola administrativa y auditoría:** Control total sobre las tablas de base de datos a través de una consola administrativa estructurada.

### 3.2. Análisis del Sistema (*System Analysis*)

La plataforma se concibe como un sistema modular interactivo donde convergen cuatro perfiles:

* **Administrador:** Supervisa la infraestructura del sistema, gestiona cuentas de usuario, audita transacciones y administra las tablas del modelo relacional.
* **Gestor (Docente / Coordinador):** Supervisa los recursos a su cargo y aprueba o rechaza solicitudes de préstamo para las actividades y proyectos de los estudiantes.
* **Usuario (Estudiante):** Consulta el catálogo de inventario disponible en el campus, solicita préstamos para sus proyectos o prácticas, y hace seguimiento de sus solicitudes.
* **Visitante:** Miembro de la comunidad o público interesado que consulta la oferta pública de recursos sin necesidad de iniciar sesión.

### 3.3. Diseño de Software y Arquitectura (*Software Design*)

TRAMA adopta una arquitectura cliente-servidor robusta, mantenible y desacoplada:

* **Backend:** Python 3.12 y Django 5.2, implementando controladores basados en vistas modulares, modelos relacionales y lógica de autenticación segura.
* **Base de Datos:** PostgreSQL 17, garantizando integridad referencial, transaccionalidad ACID y soporte para consultas concurrentes.
* **Interfaz de Usuario Central (Frontend Integrado):** Interfaz web unificada y responsiva sobre plantillas Django con sistema de diseño (*Design System*) basado en Vanilla CSS optimizado, tipografía moderna (*Plus Jakarta Sans*) y cromática profesional.
* **Capa Frontend Vite.js (Stack de Desarrollo):** Estructura de proyecto Vite.js + React 19 configurada en el repositorio (`frontend/`) para cumplir con las condiciones del stack y permitir expansiones progresivas a futuro sin duplicidad visual para el usuario.
* **Entorno de Contenedores:** Docker y Docker Compose para reproducibilidad exacta del entorno.
* **Control de Versiones:** Git con flujo de trabajo estructurado por ramas y convenciones de *Conventional Commits*.

### 3.4. Diseño de Módulos (*Module Design*)

El sistema se estructura en los siguientes módulos fundamentales:

1. **Usuarios y Autenticación (`users`):** Modelo `User` personalizado con roles nativos, relación uno-a-uno con modelo `Profile`, formularios validados y middleware de sesión.
2. **Recursos e Inventario (`resources`):** Catálogo de bienes (video beams, salas de cómputo, accesorios) con código institucional, ubicación y estado operativo.
3. **Solicitudes y Préstamos (`loans`):** Circuito de solicitud por horario, vinculación a proyectos académicos, validación docente y registro de entregas/devoluciones.
4. **Actividades y Proyectos:** Planificación de eventos académicos, jornadas, clases prácticas y defensas de grado estudiantiles.
5. **Consola Administrativa:** Panel Django Admin adaptado institucionalmente con filtros, búsquedas y permisos jerárquicos.

### 3.5. Punto de Inflexión y Codificación (*Coding*)

La construcción del código se ejecutó de forma incremental y verificada en cada etapa:

1. Orquestación del entorno de contenedores Docker (PostgreSQL 17 + Django 5.2).
2. Definición del modelo relacional de usuarios y roles universitarios.
3. Creación y ejecución de migraciones en la base de datos PostgreSQL.
4. Parametrización del panel administrativo de Django.
5. Maquetación del sistema de plantillas adaptativo según privilegios (RBAC).

---

## 4. Estado Actual: Versión 1.0 Implementada

La **Versión 1.0 de TRAMA** se encuentra completamente desplegada y funcional, cumpliendo con la totalidad de los objetivos de la primera fase:

* [x] **Stack de Desarrollo Completo (Pauta B.1):** Python 3.12, Django 5.2, PostgreSQL 17, Docker Compose y **Vite.js + React 19** en `frontend/` configurados e integrados en el repositorio.
* [x] **Presentación Unificada de Interfaz:** Para garantizar claridad durante la evaluación y evitar la confusión de dos interfaces web simultáneas, la plataforma se presenta de manera unificada a través del servicio web principal en el puerto `8000`, manteniendo los componentes y estructura de Vite.js listos en el proyecto.
* [x] **Infraestructura Contenerizada (Docker):** Orquestación integral de servicios en Docker (`trama-backend` y `trama-db`), con arranque limpio y persistencia de datos.
* [x] **Automatización de Base de Datos y Datos de Prueba:** Migraciones automáticas aplicadas al encender el contenedor y precarga inmediata de usuarios de prueba desde `initial_users.json`.
* [x] **Módulo de Usuarios (`users` — Pauta B.6):**
  * Modelo `User` personalizado heredando de `AbstractUser` con soporte para roles (`admin`, `manager`, `user`, `visitor`).
  * Modelo `Profile` con cédula, teléfono, facultad y descripción académica.
  * Formulario de Registro con validación de correo y contraseñas.
  * Formulario de Inicio de Sesión y cierre de sesión seguro.
  * Vista de Perfil de Usuario para actualización de datos.
* [x] **Django Admin Institucional (Pauta B.7):**
  * Personalizado bajo el título **`TRAMA — Administración Universitaria`**.
  * Edición de usuarios con formulario inline del perfil académico.
  * Filtros por rol, estado activo y staff; buscador por correo, usuario y nombre.
* [x] **Vistas y Plantillas Adaptativas según Roles (Pauta B.8):**
  * **Visitante:** Landing page con catálogo público y presentación de la red académica.
  * **Estudiante / Usuario:** Panel con resumen de solicitudes, préstamos activos y recursos asignados.
  * **Gestor / Docente:** Bandeja de gestión para aprobación o rechazo de solicitudes de proyectos.
  * **Administrador:** Consola de supervisión con métricas de la base de datos y acceso al panel administrativo.
* [x] **Identidad Visual Universitaria:** Paleta cromática equilibrada (Cobalto `#2563EB`, Ámbar `#F59E0B`, Azul Noche `#0B192C`), tipografía *Plus Jakarta Sans* y hoja de estilos `trama.css` modular y optimizada.

---

## 5. Cuentas de Prueba para Evaluación

Para facilitar la evaluación y demostración interactiva de los diferentes niveles de acceso y navegación basada en roles, se encuentran preconfiguradas las siguientes credenciales en la base de datos (con la contraseña unificada **`Trama2026`**):

| Rol del Sistema | Nombre del Titular | Correo Electrónico | Contraseña | Vistas y Capacidades Evaluables |
| :--- | :--- | :--- | :--- | :--- |
| **Administrador** | Carlos Mendoza | `admin@trama.local` | `Trama2026` | Consola global, métricas de PostgreSQL y acceso al [Django Admin](http://127.0.0.1:8000/admin/). |
| **Gestor / Docente** | Prof. Rafael Barrios | `docente@trama.local` | `Trama2026` | Panel de gestión, bandeja de aprobación de solicitudes y control de recursos docentes. |
| **Estudiante** | Mariana Silva | `estudiante@trama.local` | `Trama2026` | Panel del estudiante, estado de solicitudes personales y vinculación a proyectos académicos. |
| **Visitante** | *Público General* | *(Sin iniciar sesión)* | N/A | Consulta del catálogo de recursos, descripción de la plataforma y accesos a registro/login. |

---

## 6. Guía de Instalación y Ejecución con Docker

### Requisitos Previos
* [Docker Desktop](https://www.docker.com/) instalado y en ejecución.
* Git instalado en el sistema.

### Instrucciones de Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/alejose2050-afk/TRAMA.git
   cd TRAMA
   ```

2. **Iniciar los servicios con Docker Compose:**
   ```bash
   docker compose up -d
   ```

3. **Verificar el estado de los contenedores:**
   ```bash
   docker compose ps
   ```
   *Deberá observar `trama-backend` (puerto `8000`) y `trama-db` (puerto `5432`) en estado activo (`Up`).*

4. **Acceder a la plataforma web única:**
   * **Plataforma Web TRAMA:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   * **Panel Administrativo (Django Admin):** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

   *(El módulo `frontend/` basado en Vite.js y React se encuentra listo en el repositorio para futuras expansiones como SPA).*

5. **Detener los servicios cuando sea necesario:**
   ```bash
   docker compose down
   ```

---

## 7. Estructura del Proyecto

```text
trama-platform/
├── backend/                        # Código fuente del backend Django
│   ├── config/                     # Configuración principal del proyecto
│   │   ├── asgi.py
│   │   ├── settings.py             # Configuración central (DB, Auth, Apps)
│   │   ├── urls.py                 # Enrutador global y títulos del Admin
│   │   └── wsgi.py
│   ├── static/                     # Archivos estáticos institucionales
│   │   ├── css/
│   │   │   └── trama.css           # Sistema de diseño e identidad visual
│   │   └── img/
│   │       └── trama_logo.png      # Logo oficial de TRAMA
│   ├── templates/                  # Sistema de plantillas HTML
│   │   ├── base.html               # Plantilla maestra con navbar institucional
│   │   ├── home.html               # Despachador de vistas por rol
│   │   ├── roles/                  # Vistas modulares según perfil
│   │   │   ├── dashboard_admin.html
│   │   │   ├── dashboard_manager.html
│   │   │   ├── dashboard_user.html
│   │   │   └── landing_visitor.html
│   │   └── users/                  # Vistas de autenticación
│   │       ├── login.html
│   │       ├── profile.html
│   │       └── register.html
│   ├── users/                      # Aplicación Django de Usuarios y Autenticación
│   │   ├── fixtures/
│   │   │   └── initial_users.json  # Cuentas de prueba precargadas automáticamente
│   │   ├── admin.py                # Configuración de tablas en Django Admin
│   │   ├── forms.py                # Formularios de Registro, Login y Perfil
│   │   ├── models.py               # Modelos User y Profile con roles
│   │   ├── urls.py                 # Rutas de autenticación
│   │   └── views.py                # Controladores y lógica RBAC
│   ├── Dockerfile                  # Imagen Docker para el entorno Python
│   ├── manage.py
│   └── requirements.txt            # Dependencias del backend
├── frontend/                       # Código fuente del frontend (Vite.js + React)
│   ├── public/                     # Recursos estáticos públicos (logo, iconos)
│   ├── src/                        # Código fuente React (App, estilos, componentes)
│   ├── Dockerfile                  # Imagen Docker para el entorno Node/Vite
│   ├── package.json                # Dependencias de Vite y React
│   └── vite.config.js              # Configuración del servidor de desarrollo Vite
├── compose.yaml                    # Orquestación de servicios (Django + Postgres)
└── README.md                       # Documentación técnica y académica del proyecto
```

---

## 8. Organización y Flujo de Trabajo

El desarrollo se gestiona de forma incremental:
* La rama **`main`** alberga las versiones estables y verificadas del software.
* Se utilizan ramas de funcionalidad (*feature branches*) para el desarrollo de módulos específicos.
* Cada cambio significativo se documenta mediante commits concisos y verificación en contenedores.

---

## 9. Objetivo de la Metodología

La aplicación sistemática de la **metodología de desarrollo en V** garantiza la correspondencia directa entre los requisitos levantados, la arquitectura tecnológica, el código implementado y las futuras fases de pruebas unitarias y de integración. De esta manera, se asegura la construcción de una plataforma estable, segura, escalable y estrechamente vinculada a las necesidades operativas de la comunidad universitaria.
