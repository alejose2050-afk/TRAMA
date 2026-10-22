# TRAMA
## Plataforma Integral de Gestión y Articulación de Recursos Universitarios

> ### 📌 Nota para el Docente / Evaluación Académica
> **Profesor Rafael Barrios:** Aquí se encuentran implementadas y organizadas las condiciones previstas que colocó en el Classroom para el desarrollo del proyecto. Si de alguna manera esta primera fase se aprecia más desarrollada de lo pedido inicialmente, el motivo es porque estoy a punto de quedarme temporalmente sin computadora y quería dejar las cosas lo más adelantadas y estructuradas posible para poder migrarme a mi nuevo dispositivo prontamente. Ya que no tengo una fecha estimada exacta de cuándo me llega la nueva o cuándo me quedo sin mi computadora actual, quise dejar todo lo más adelantado posible para no tener problemas en el futuro con las próximas entregas.

---

## 1. Génesis y Origen de TRAMA

**TRAMA** no surge como una idea aislada, sino como el punto de convergencia y evolución de tres vertientes y experiencias de desarrollo previas:

1. **Gestión y Organización de Tareas (Proyecto de Semestre Anterior):** La experiencia previa en el desarrollo de herramientas para el seguimiento de tareas, asignación de responsabilidades y flujos de trabajo secuenciales sentó las bases para el control de estados y autorizaciones.
2. **Administración de Recursos y Gestión (Proyecto Personal):** El diseño de una solución personal orientada al control financiero, balances y optimización de activos aportó la lógica para el seguimiento de disponibilidad, inventario y rendición de cuentas de bienes.
3. **Planificación y Coordinación Universitaria (Proyectos de Grado y Subproyectos):** La necesidad cotidiana de estudiantes y docentes de la UNELLEZ de coordinar defensas de grado, prácticas académicas y disponer de recursos tecnológicos (video beams, salas de cómputo, auditorios) sin fricciones ni desorganización.

La integración de estas tres visiones dio nacimiento a **TRAMA**: una plataforma centralizada que articula el préstamo de bienes institucionales, la validación docente y el respaldo a los subproyectos académicos de la comunidad unellista.

---

## 2. Introducción

TRAMA es una plataforma web orientada a facilitar la organización de actividades universitarias y la coordinación de recursos entre los miembros de la comunidad académica. Su propósito es centralizar la publicación de recursos, la gestión de solicitudes y el seguimiento de préstamos relacionados con actividades universitarias.

Para orientar su desarrollo, se utiliza la **metodología de desarrollo en V**, siguiendo la rama descendente para definir progresivamente los requisitos, la arquitectura y el diseño del sistema antes de comenzar la implementación del código.

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

En esta etapa se identificaron las necesidades de los usuarios y las funcionalidades requeridas para TRAMA en el contexto universitario:

* **Registro, inicio de sesión y gestión de perfiles:** Identificación por correo institucional, cédula de identidad, teléfono y adscripción al subprograma académico.
* **Administración de roles y permisos (RBAC):** Separación estricta de privilegios entre Administrador, Gestor, Usuario y Visitante.
* **Publicación y consulta de recursos disponibles:** Catálogo de equipos audiovisuales, laboratorios y espacios físicos de la sede.
* **Coordinación de solicitudes y préstamos:** Solicitud formal de equipos vinculada a subproyectos académicos, con validación de disponibilidad y aprobación del responsable.
* **Seguimiento del estado de solicitudes:** Trazabilidad en tiempo real (*Pendiente*, *Aprobado*, *Rechazado*, *Finalizado*).
* **Gestión de presupuestos y recursos asociados:** Estimación y control de insumos requeridos para eventos y prácticas académicas.
* **Administración y auditoría:** Control total sobre las tablas de base de datos a través de una consola administrativa institucional.

### 3.2. Análisis del Sistema (*System Analysis*)

La plataforma se concibe como un sistema modular interactivo donde convergen cuatro perfiles claramente diferenciados:

* **Administrador:** Supervisa la infraestructura del sistema, gestiona cuentas de usuario, audita transacciones y administra las tablas del modelo relacional.
* **Gestor (Docente / Jefe de Subprograma):** Supervisa los recursos a su cargo (ej. laboratorios de computación o equipos de jefatura) y aprueba o rechaza solicitudes de préstamo para las actividades y subproyectos.
* **Usuario (Estudiante):** Consulta el catálogo de inventario disponible en el campus, solicita préstamos para sus subproyectos y defensas de grado, y hace seguimiento de sus solicitudes.
* **Visitante:** Miembro de la comunidad universitaria o externo que consulta la oferta institucional pública de recursos sin necesidad de iniciar sesión.

### 3.3. Diseño de Software y Arquitectura (*Software Design*)

TRAMA adopta una arquitectura cliente-servidor robusta, mantenible y desacoplada:

* **Backend:** Python 3.12 y Django 5.2, implementando controladores basados en vistas modulares, modelos relacionales y lógica de autenticación segura.
* **Base de Datos:** PostgreSQL 17, garantizando integridad referencial, transaccionalidad ACID y soporte para consultas concurrentes.
* **Frontend:** Interfaz web responsiva con sistema de diseño institucional (*Design System*) basado en Vanilla CSS optimizado, tipografía oficial (*Plus Jakarta Sans*) y cromática institucional UNELLEZ. Preparado para integración progresiva con React / Vite.
* **Entorno de Contenedores:** Docker y Docker Compose para reproducibilidad exacta del entorno tanto en desarrollo como en producción.
* **Control de Versiones:** Git con flujo de trabajo estructurado por ramas y convenciones de *Conventional Commits*.

### 3.4. Diseño de Módulos (*Module Design*)

El sistema se estructura en los siguientes módulos fundamentales:

1. **Usuarios y Autenticación (`users`):** Modelo `User` personalizado con roles nativos, relación uno-a-uno con modelo `Profile`, formularios validados y middleware de sesión.
2. **Recursos e Inventario (`resources`):** Catálogo de bienes (video beams, salas de computación, accesorios) con código de bien institucional, sede y estado de operatividad.
3. **Solicitudes y Préstamos (`loans`):** Circuito de solicitud por horario, vinculación a subproyecto académico, validación docente y registro de entregas/devoluciones.
4. **Actividades y Subproyectos:** Planificación de eventos académicos, jornadas, clases prácticas y defensas de proyecto vinculadas al uso de bienes.
5. **Presupuestos y Planificación:** Estimación y control de costos asociados al uso o mantenimiento de recursos.
6. **Consola Administrativa:** Panel Django Admin personalizado institucionalmente con filtros, búsquedas y permisos jerárquicos.

### 3.5. Punto de Inflexión

El punto de inflexión marcó la culminación formal de la fase de planificación y especificación técnica, dando paso inmediato a la construcción del software ejecutable sobre infraestructura de contenedores.

### 3.6. Codificación (*Coding*)

La construcción del código se ejecutó de forma incremental y verificada en cada etapa:

1. Orquestación del entorno de contenedores Docker (PostgreSQL 17 + Django 5.2).
2. Definición del modelo relacional de usuarios y roles con soporte para adscripción a la UNELLEZ.
3. Creación y ejecución de migraciones en la base de datos PostgreSQL.
4. Parametrización del panel administrativo de Django con identidad institucional.
5. Maquetación del sistema de plantillas adaptativo según privilegios (RBAC).

---

## 4. Estado Actual: Versión 1.0 Implementada

La **Versión 1.0 de TRAMA** se encuentra completamente desplegada y funcional, cumpliendo con la totalidad de los objetivos de la primera fase:

* [x] **Stack de Desarrollo Completo (Pauta B.1):** Python 3.12, Django 5.2, PostgreSQL 17, Docker Compose y **Vite.js + React 19** en `frontend/` descargados, instalados y orquestados.
* [x] **Infraestructura Contenerizada (Docker):** Orquestación integral de 3 servicios: `trama-backend` (Django), `trama-db` (PostgreSQL 17) y `trama-frontend` (Vite.js).
* [x] **Automatización de Base de Datos y Datos de Prueba:** Migraciones automáticas aplicadas al encender el contenedor y precarga inmediata de usuarios de prueba desde `initial_users.json`.
* [x] **Base de Datos Relacional:** PostgreSQL 17 conectado y sincronizado mediante migraciones Django.
* [x] **Módulo de Usuarios (`users` — Pauta B.6):**
  * Modelo `User` personalizado heredando de `AbstractUser` con soporte para roles (`admin`, `manager`, `user`, `visitor`).
  * Modelo `Profile` con cédula, teléfono, subprograma y subproyecto.
  * Formulario de Registro con validación de correo institucional y contraseñas.
  * Formulario de Inicio de Sesión y cierre de sesión seguro.
  * Vista de Perfil de Usuario para actualización de datos académicos.
* [x] **Django Admin Institucional (Pauta B.7):**
  * Personalizado bajo el título **`TRAMA — Administración UNELLEZ`**.
  * Edición de usuarios con formulario inline del perfil académico.
  * Filtros por rol, estado activo y staff; buscador por correo, usuario y nombre.
* [x] **Vistas y Plantillas Adaptativas según Roles (Pauta B.8):**
  * **Visitante:** Landing page con catálogo público y presentación de la red académica.
  * **Estudiante / Usuario:** Panel con resumen de solicitudes, préstamos activos y recursos asignados.
  * **Gestor / Docente:** Bandeja de gestión para aprobación o rechazo de solicitudes de subproyectos.
  * **Administrador:** Consola de supervisión con métricas de la base de datos y acceso al panel administrativo.
* [x] **Frontend SPA con Vite.js y React 19 (Puerto 5173):** Aplicación cliente lista para el consumo de datos, con interfaz institucional unellista y verificación interactiva de conexión con el backend.
* [x] **Identidad Visual UNELLEZ:** Paleta cromática oficial (Cobalto `#2563EB`, Ámbar `#F59E0B`, Azul Noche `#0B192C`), tipografía *Plus Jakarta Sans* y hoja de estilos `trama.css` modular y optimizada (316 líneas, 0 advertencias).

---

## 5. Cuentas de Prueba para Evaluación

Para facilitar la evaluación y demostración interactiva de los diferentes niveles de acceso y navegación basada en roles, se encuentran preconfiguradas las siguientes credenciales en la base de datos:

| Rol del Sistema | Nombre de Usuario / Titular | Correo Electrónico | Contraseña | Vistas y Capacidades Evaluables |
| :--- | :--- | :--- | :--- | :--- |
| **Administrador** | Admin TRAMA | `admin@trama.local` | `TramaDev2026!` | Consola global, métricas de PostgreSQL y acceso al [Django Admin](http://127.0.0.1:8000/admin/). |
| **Gestor / Docente** | Prof. Carlos Mendoza | `docente@trama.local` | `TramaDev2026!` | Panel de gestión, bandeja de aprobación de solicitudes y control de recursos del subprograma. |
| **Estudiante** | María Fernández | `estudiante@trama.local` | `TramaDev2026!` | Panel del estudiante, estado de solicitudes personales y vinculación a subproyectos. |
| **Visitante** | *Público General* | *(Sin iniciar sesión)* | N/A | Consulta del catálogo de recursos, descripción de la plataforma y accesos a registro/login. |

> **Nota:** También se encuentran activas las cuentas de desarrollo alternativas `alejose2050@gmail.com` (Gestor) y `alejandro.g@universidad.edu` (Estudiante), ambas con la contraseña `TramaDev2026!`.

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
   *Deberá observar `trama-backend` (puerto `8000`), `trama-db` (puerto `5432`) y `trama-frontend` (puerto `5173`) en estado activo (`Up`).*

4. **Acceder a los módulos del stack:**
   * **Plataforma Web (Portal TRAMA - Django):** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   * **Panel Administrativo (Django Admin):** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
   * **Entorno Cliente SPA (Vite.js + React):** [http://127.0.0.1:5173/](http://127.0.0.1:5173/)

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
│   │   │   └── trama.css           # Sistema de diseño e identidad visual (UNELLEZ)
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
├── compose.yaml                    # Orquestación de servicios (Django + Postgres + Vite)
└── README.md                       # Documentación técnica y académica del proyecto
```

---

## 8. Organización y Flujo de Trabajo

El desarrollo se gestiona de forma incremental:
* La rama **`main`** alberga las versiones estables y verificadas del software.
* Se utilizan ramas de funcionalidad (*feature branches*) para el desarrollo de módulos específicos.
* Cada cambio significativo se documenta mediante commits semánticos y verificación cruzada en contenedores.

---

## 9. Objetivo de la Metodología

La aplicación sistemática de la **metodología de desarrollo en V** garantiza la correspondencia directa entre los requisitos levantados, la arquitectura tecnológica, el código implementado y las futuras fases de pruebas unitarias y de integración. De esta manera, se asegura la construcción de una plataforma estable, segura, escalable y estrechamente vinculada a las necesidades operativas de la comunidad académica de la UNELLEZ.
