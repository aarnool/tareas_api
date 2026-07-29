[🇬🇧 English](README.md) | [🇪🇸 Español](README-es.md)    

# 🚀 API de Tareas Simples (Task Management API)

![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.139.2+-00a393.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)
![MySQL](https://img.shields.io/badge/MySQL-Soportado-blue)
![License](https://img.shields.io/badge/Licencia-MIT-green.svg)

Una API RESTful robusta construida con **FastAPI** y **SQLAlchemy** para la gestión eficiente de usuarios y tareas. Cuenta con autenticación segura basada en JWT, aislamiento de datos por usuario y documentación de la API completa lista para usarse.

---

## 📑 Tabla de Contenidos
- [✨ Características](#-características)
- [🛠️ Tecnologías Utilizadas](#️-tecnologías-utilizadas)
- [⚙️ Instalación y Configuración](#️-instalación-y-configuración)
- [🔑 Variables de Entorno](#-variables-de-entorno)
- [🌐 Endpoints de la API](#-endpoints-de-la-api)
- [🏛️ Diagramas y Arquitectura](#️-diagramas-y-arquitectura)
- [📸 Capturas de Pantalla y Ejemplos](#-capturas-de-pantalla-y-ejemplos)
- [📂 Estructura del Proyecto](#-estructura-del-proyecto)

---

## ✨ Características

- **Autenticación de Usuarios**: Registro y login seguros usando OAuth2 con contraseñas encriptadas (hashed).
- **Autorización JWT**: Gestión de sesiones usando cookies seguras (HTTP-only).
- **Aislamiento de Datos**: Los usuarios solo pueden acceder y modificar sus propias tareas.
- **Paginación**: Recuperación eficiente de datos con soporte de paginación integrado para las tareas.
- **Validación**: Estricta validación de datos en peticiones y respuestas mediante Pydantic.
- **Migraciones de Base de Datos**: Gestión del esquema de base de datos de manera impecable usando Alembic.

---

## 🛠️ Tecnologías Utilizadas

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Framework web rápido para construir APIs con Python.
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) - Object Relational Mapper para una interacción robusta con la base de datos.
- **Base de Datos**: [PyMySQL](https://pymysql.readthedocs.io/) - Conector de Python para bases de datos MySQL síncronas.
- **Validación**: [Pydantic](https://docs.pydantic.dev/) - Validación de datos y gestión de configuraciones.
- **Migraciones**: [Alembic](https://alembic.sqlalchemy.org/) - Herramienta ligera para migraciones de bases de datos.

---

## ⚙️ Instalación y Configuración

### 1. Requisitos previos
Asegúrate de tener instalado **Python 3.14 o superior**.

### 2. Entorno Virtual
Se recomienda encarecidamente usar un entorno virtual. Este proyecto utiliza `uv` para una gestión rápida de dependencias, pero `pip` tradicional también funciona perfectamente.

```bash
# Usando uv (Recomendado)
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Usando pip tradicional
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Migraciones de Base de Datos
Antes de ejecutar la aplicación, asegúrate de que tu base de datos esté activa y aplica las migraciones usando Alembic para crear las tablas necesarias:

```bash
alembic upgrade head
```

### 4. Ejecutar la Aplicación
Puedes iniciar el servidor de desarrollo localmente con el siguiente comando (usando `fastapi-cli`):

```bash
fastapi dev src/main.py
```

La API estará disponible en `http://localhost:8000`.
Puedes explorar la documentación interactiva de la API (Swagger UI) en `http://localhost:8000/docs`.

> 💡 **Demo en Vivo:** Puedes acceder a la documentación interactiva sin necesidad de clonar el proyecto en [https://tareas-api-lc94.onrender.com/docs](https://tareas-api-lc94.onrender.com/docs).
> *Nota: Si la documentación demora unos segundos en responder durante la primera carga, se debe a que el backend está desplegado en una instancia gratuita de Render y entra en reposo tras un periodo de inactividad. ¡Agradecemos tu paciencia mientras se reactiva!*

---

## 🔑 Variables de Entorno

Para ejecutar este proyecto localmente con una base de datos real, debes crear un archivo `.env` en la raíz del proyecto basándote en el archivo `.env.example` proporcionado:

```env
DB_USER=tu_usuario_bd
DB_PASSWORD=tu_contraseña_bd
DB_HOST=localhost
DB_PORT=3306
DB_NAME=tu_nombre_bd
SECRET_KEY=tu_super_clave_secreta
FRONTEND_URL=http://localhost:3000
```

---

## 🌐 Endpoints de la API

### 🩺 Verificación y Raíz
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Endpoint raíz para verificar que la API está funcionando correctamente. |

### 👤 Usuarios (Autenticación y Gestión)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/users/register` | Registra una nueva cuenta de usuario. Valida que el nombre de usuario y correo sean únicos, y encripta la contraseña. |
| `POST` | `/users/login` | Autentica a un usuario mediante credenciales OAuth2 y configura una cookie segura HTTP-only con el token JWT (`auth_token`). |
| `GET` | `/users/me` | Obtiene los datos del perfil del usuario actualmente autenticado (requiere la cookie `auth_token` válida). |
| `POST` | `/users/logout` | Cierra la sesión del usuario eliminando la cookie de autenticación. |

### 📝 Tareas (Aislamiento por Usuario)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/tasks` | Crea una nueva tarea asociada al usuario autenticado (estado por defecto `pending`, prioridad por defecto `medium`). |
| `GET` | `/tasks` | Obtiene una lista paginada de todas las tareas del usuario autenticado. Admite parámetros de paginación `start` y `limit`. |
| `PATCH`| `/tasks/{task_id}`| Actualiza parcial o totalmente los campos de una tarea por ID. Restringido al propietario de la tarea. |
| `DELETE`| `/tasks/{task_id}`| Elimina una tarea por su ID. Restringido al propietario de la tarea. |

---

## 🏛️ Diagramas y Arquitectura

### Modelo Físico
![Modelo Físico](public/physical_model.png)

### Diagrama de Secuencia: Creación de Token JWT
![Diagrama de Secuencia](public/sequence_diagram.png)

### Diagrama de Flujo: Creación de Cuenta
![Diagrama de Flujo 1](public/flowchart(1).png)

### Endpoints Protegidos (Requieren JWT)
![Diagrama de Flujo 2](public/flowchart(2).png)

---

## 📸 Capturas de Pantalla y Ejemplos

### Documentación de la API (Swagger UI)
![Documentación de la API](public/doc.png)

### Ejemplo de Caso de Uso (Frontend)
Puedes probar la aplicación del frontend en vivo desde el siguiente enlace: **[Demostración del Frontend](https://frontend-seven-livid-1rwmj8gd6q.vercel.app/)**

![Vista del Frontend](public/ejem.png)

> 💡 **Nota Importante:** Si el frontend demora unos segundos en responder durante la primera carga, se debe a que el backend está desplegado en una instancia gratuita de Render y entra en reposo tras un periodo de inactividad. ¡Agradecemos tu paciencia mientras se reactiva!

---

## 📂 Estructura del Proyecto

```text
├── alembic/              # Database migrations configuration and versions
├── docs/                 # Documentation files and assets
│   ├── README.md
│   └── README-es.md
├── src/                  # Main source code
│   ├── core/             # Cross-cutting functionalities (security, custom exceptions)
│   ├── domains/          # Business logic separated by domains (users, tasks)
│   ├── config.py         # App configuration & environment variables settings
│   ├── database.py       # Database connection & SQLAlchemy session management
│   ├── dependencies.py   # Global FastAPI dependencies (e.g., get_db, get_current_user)
│   ├── main.py           # FastAPI entry point, CORS, router registration
│   └── models.py         # Aggregator for ORM models (used by Alembic)
├── tests/                # Automated unit and integration tests (Pytest)
├── .env                  # Environment variables (not in VCS)
├── .env.example          # Template for environment variables
├── alembic.ini           # Alembic configuration file
├── pyproject.toml        # Project metadata and dependencies
└── requirements.txt      # Standard requirements file
```
