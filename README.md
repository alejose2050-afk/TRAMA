# TRAMA
## Plataforma Integral de Gestión y Articulación de Recursos Universitarios

### 1. Introducción

TRAMA es una plataforma web orientada a facilitar la organización de actividades universitarias y la coordinación de recursos entre los miembros de la comunidad académica. Su propósito es centralizar la publicación de recursos, la gestión de solicitudes y el seguimiento de préstamos relacionados con actividades universitarias.

Para orientar su desarrollo, se utilizará la **metodología de desarrollo en V**, siguiendo la rama descendente para definir progresivamente los requisitos, la arquitectura y el diseño del sistema antes de comenzar la implementación del código.

## 2. Metodología de desarrollo en V

### 2.1. Análisis de Requisitos (*Requirement Gathering*)

En esta etapa se identificarán las necesidades de los usuarios y las funcionalidades que deberá ofrecer TRAMA.

Entre los requisitos funcionales iniciales se encuentran:

- Registro, inicio de sesión y gestión de usuarios.
- Administración de roles y permisos.
- Publicación y consulta de recursos universitarios disponibles.
- Creación y organización de actividades universitarias.
- Solicitud y coordinación de préstamos de recursos.
- Seguimiento del estado de las solicitudes.
- Gestión de presupuestos asociados a las actividades.
- Administración general de la plataforma.

El sistema deberá garantizar que las solicitudes de recursos requieran la aceptación de la persona responsable antes de considerarse aprobadas. También se tendrán en cuenta requisitos no funcionales como la seguridad, la facilidad de uso, la integridad de los datos y la mantenibilidad del software.

### 2.2. Análisis del Sistema (*System Analysis*)

En esta fase se definirá el comportamiento general de TRAMA y la forma en que interactuarán sus componentes.

La plataforma contará con una interfaz web para los usuarios, un backend encargado de procesar las operaciones y una base de datos para almacenar la información.

El funcionamiento general contemplará el registro de usuarios, la publicación de recursos, la organización de actividades y la creación y gestión de solicitudes. Cada operación estará sujeta a las reglas del sistema y a los permisos correspondientes al rol del usuario.

Se contemplan los siguientes perfiles:

- **Administrador:** supervisa la plataforma y administra sus configuraciones y registros.
- **Gestor:** organiza actividades y coordina los recursos relacionados con ellas, de acuerdo con sus permisos.
- **Usuario:** consulta recursos, publica los que puede ofrecer y realiza solicitudes.
- **Visitante:** accede únicamente a las funcionalidades públicas permitidas.

Una misma persona podrá ofrecer recursos y solicitar otros, siempre que cumpla las condiciones establecidas por el sistema.

### 2.3. Diseño de Software y Arquitectura (*Software Design*)

En esta etapa se establecerá la arquitectura tecnológica y la comunicación entre los componentes de TRAMA.

Se propone una arquitectura cliente-servidor dividida en las siguientes partes:

- **Frontend:** React y Vite para construir la interfaz web y facilitar la interacción con los usuarios.
- **Backend:** Python, Django y Django REST Framework para implementar la lógica de negocio, la autenticación, los permisos y las API.
- **Base de datos:** PostgreSQL para almacenar usuarios, actividades, recursos, solicitudes y presupuestos.
- **Entorno de desarrollo:** Docker y Docker Compose para configurar y ejecutar los servicios de forma reproducible.
- **Control de versiones:** Git y GitHub para registrar los cambios, gestionar ramas y mantener el historial del desarrollo.

La arquitectura mantendrá separadas la interfaz, las reglas de negocio y la persistencia de datos, facilitando las pruebas, el mantenimiento y la incorporación de nuevas funcionalidades.

Estas tecnologías constituyen la propuesta inicial y se verificarán durante la preparación del entorno.

### 2.4. Diseño de Módulos (*Module Design*)

En esta fase se detallará la estructura interna de cada módulo, sus responsabilidades, los modelos de datos y las reglas que deberá cumplir.

Los módulos iniciales previstos son:

1. **Usuarios y autenticación:** registro, inicio de sesión, perfiles y asignación de roles.
2. **Actividades:** creación, consulta, actualización y seguimiento de actividades universitarias.
3. **Recursos:** publicación, descripción, consulta y administración de recursos disponibles.
4. **Solicitudes y préstamos:** registro de solicitudes, aceptación o rechazo por parte del responsable y seguimiento de los estados.
5. **Presupuestos:** registro y consulta de presupuestos vinculados a actividades.
6. **Administración:** gestión de registros y supervisión de la plataforma mediante permisos administrativos.

También se definirán las relaciones entre los modelos de datos. Por ejemplo, una actividad podrá estar asociada a varias solicitudes de recursos, mientras que cada solicitud deberá identificar el recurso solicitado, la persona solicitante y su estado.

Las reglas de validación evitarán solicitudes inconsistentes, operaciones no autorizadas y aprobaciones que no hayan sido confirmadas por la persona responsable.

### 2.5. Punto de Inflexión

El punto de inflexión representa la transición entre la planificación y el diseño del sistema, en la rama descendente, y la construcción del software.

Antes de comenzar la codificación, se revisarán los requisitos, la arquitectura propuesta, los módulos definidos y las tecnologías seleccionadas. Esta revisión permitirá detectar inconsistencias y reducir cambios importantes durante la implementación.

Una vez validada la planificación, se iniciará el desarrollo progresivo de TRAMA, comenzando por la configuración del entorno, la estructura del backend, la autenticación y los componentes fundamentales del sistema.

### 2.6. Codificación (*Coding*)

En esta etapa se construirá el código fuente de TRAMA siguiendo los diseños y especificaciones establecidos previamente.

El desarrollo se organizará por módulos y se gestionará mediante Git y GitHub, utilizando ramas para separar las funcionalidades y registrando los cambios mediante commits descriptivos.

La implementación comenzará con:

- Preparación y configuración del entorno de desarrollo con Docker.
- Creación de la estructura del proyecto Django.
- Configuración de la base de datos.
- Desarrollo del registro, inicio de sesión y gestión de roles.
- Configuración del panel administrativo de Django.
- Construcción de las vistas y la interfaz web.
- Implementación progresiva de los módulos de actividades, recursos, solicitudes y presupuestos.

Cada componente se comprobará durante su desarrollo para detectar errores y facilitar su integración. Posteriormente, se realizarán pruebas funcionales y de integración relacionadas con los requisitos definidos.

## 3. Organización del desarrollo

El proyecto se desarrollará de forma incremental, priorizando primero la infraestructura y las funciones esenciales. Las funcionalidades se incorporarán progresivamente y se documentarán los cambios importantes.

La rama `main` se reservará para versiones estables del proyecto, mientras que las ramas de trabajo permitirán desarrollar y revisar funcionalidades antes de integrarlas.

## 4. Estado actual del proyecto

TRAMA se encuentra en la fase inicial de preparación del entorno y organización del desarrollo. Los requisitos y módulos descritos corresponden a la planificación inicial; su implementación y validación se realizarán progresivamente.

## 5. Objetivo de la metodología

La aplicación de la metodología de desarrollo en V permitirá mantener una relación clara entre los requisitos, el diseño, la implementación y las pruebas del sistema. De esta manera, se busca construir una plataforma organizada, segura, mantenible y adaptada a las necesidades de la comunidad universitaria.
