[🇬🇧 Ingles](README.md)    [🇪🇸 Español](README-es.md)    
# API de Tareas Simples (Task Management API)

Esta es una API RESTful construida con **FastAPI** y **SQLAlchemy** para la gestión de usuarios y tareas. 

## Tecnologías Utilizadas

- **FastAPI**: Framework web rápido para construir APIs con Python.
- **SQLAlchemy**: ORM (Object Relational Mapper) para la interacción con la base de datos.
- **PyMySQL**: Conector de Python para bases de datos MySQL sincrono .
- **Pydantic**: Validación de datos y gestión de configuraciones.

## ⚙️ Instalación y Configuración

### 1. Requisitos previos
Asegúrate de tener instalado **Python 3.14 o superior**.

2. **Entorno Virtual**:
   Se recomienda usar un entorno virtual y administrar las dependencias utilizando el archivo `pyproject.toml` (este proyecto utiliza `uv`) o el archivo `requirements.txt` (para `pip` tradicional).

3. **Ejecutar la aplicación**:
   Puedes iniciar el servidor localmente con el siguiente comando (gracias a `fastapi-cli`):
   ```bash
   fastapi dev src/main.py
   ```
   La API estará disponible en `http://localhost:8000`. 
   Puedes acceder a la documentación interactiva (Swagger UI) sin clonar ni ejecutar en `https://tareas-api-lc94.onrender.com/docs`.

> **Nota Importante:** Si la documentacion demora unos segundos en responder durante la primera carga, se debe a que el backend está desplegado en una instancia gratuita de Render y entra en reposo tras un periodo de inactividad. ¡Agradecemos tu paciencia mientras se reactiva!



## Endpoints de la API

### Raíz (Root)
- **`GET /`**: Endpoint raíz de verificación para comprobar que la API está funcionando correctamente.

### Usuarios (Users - Autenticación y Gestión)
- **`POST /users/register`**: Registra una nueva cuenta de usuario (valida que el usuario y correo sean únicos y cifra la contraseña).
- **`POST /users/login`**: Autentica al usuario mediante credenciales OAuth2 (correo/usuario y contraseña) y configura una cookie segura HTTP-only JWT (`auth_token`).
- **`GET /users/me`**: Obtiene los datos del perfil del usuario actualmente autenticado (requiere cookie `auth_token` válida).
- **`POST /users/logout`**: Cierra la sesión del usuario eliminando la cookie de autenticación.

### Tareas (Tasks - Aislamiento por Usuario)
- **`POST /tasks`**: Crea una nueva tarea asociada al usuario autenticado (estado por defecto `pending`, prioridad por defecto `medium`).
- **`GET /tasks`**: Obtiene una lista paginada de todas las tareas pertenecientes al usuario autenticado (admite parámetros de paginación `start` y `limit`).
- **`PATCH /tasks/{task_id}`**: Actualiza parcial o totalmente los campos de una tarea por ID (restringido al propietario de la tarea).
- **`DELETE /tasks/{task_id}`**: Elimina una tarea por su ID (restringido al propietario de la tarea).

## 🏛️ Diagramas y Arquitectura

### Modelo Físico
![Modelo Físico](public/physical_model.png)

### Diagrama de Secuencia: Creación de Token JWT
![Diagrama de Secuencia](public/sequence_diagram.png)

### Diagrama de Flujo: Creación de Cuenta
![Diagrama de Flujo 1](public/flowchart(1).png)

### Endpoints Protegidos (Requieren JWT)
![Diagrama de Flujo 2](public/flowchart(2).png)

## Capturas de Pantalla / Ejemplos

### Documentación de la API (Swagger UI)
![Documentación de la API](public/doc.png)

### Ejemplo de Caso de Uso (Frontend)
Puedes probar la aplicación del frontend en vivo desde el siguiente enlace: **[Demostración del Frontend](https://frontend-seven-livid-1rwmj8gd6q.vercel.app/)**

![Vista del Frontend](public/ejem.png)

> **Nota Importante:** Si el frontend demora unos segundos en responder durante la primera carga, se debe a que el backend está desplegado en una instancia gratuita de Render y entra en reposo tras un periodo de inactividad. ¡Agradecemos tu paciencia mientras se reactiva!

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
