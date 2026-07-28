[🇬🇧 Ingles](README.md)    [🇪🇸 Español](README-es.md)    
# API de Tareas Simples (Task Management API)

Esta es una API RESTful construida con **FastAPI** y **SQLAlchemy** para la gestión de usuarios y tareas. 

## Tecnologías Utilizadas

- **FastAPI**: Framework web rápido para construir APIs con Python.
- **SQLAlchemy**: ORM (Object Relational Mapper) para la interacción con la base de datos.
- **PyMySQL**: Conector de Python para bases de datos MySQL sincrono .
- **Pydantic**: Validación de datos y gestión de configuraciones.

## Instalación y Configuración

1. **Requisitos previos**:
   Asegúrate de tener Python 3.14 o superior instalado.

2. **Entorno Virtual**:
   Se recomienda usar un entorno virtual y administrar las dependencias utilizando el archivo `pyproject.toml` (este proyecto utiliza `uv`) o el archivo `requirements.txt` (para `pip` tradicional).

3. **Ejecutar la aplicación**:
   Puedes iniciar el servidor localmente con el siguiente comando (gracias a `fastapi-cli`):
   ```bash
   fastapi dev src/main.py
   ```
   La API estará disponible en `http://localhost:8000`. 
   Puedes acceder a la documentación interactiva (Swagger UI) en `http://localhost:8000/docs`.

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

## Diagramas y Arquitectura

### Modelo Físico
![Modelo Físico](public/physical_model.png)

### Diagrama de Secuencia de como la API crea un Token JWT
![Diagrama de Secuencia](public/sequence_diagram.png)

### Diagramas de Flujo de la creación de una cuenta
![Diagrama de Flujo 1](public/flowchart(1).png)

## END-POINTS permitidos con el token JWT
![Diagrama de Flujo 2](public/flowchart(2).png)

## Capturas de Pantalla / Ejemplos

### Documentación de la API (Swagger)
![Documentación de la API](public/doc.png)

### Ejemplo de Caso de Uso (Frontend)
Puedes probar la aplicación en vivo desde el siguiente enlace: [Demostración del Frontend](https://frontend-seven-livid-1rwmj8gd6q.vercel.app/))

![Vista del Frontend](public/ejem.png)

> **Nota Importante:** Si el frontend demora unos segundos en responder durante la primera carga, se debe a que el backend está desplegado en una instancia gratuita de Render y entra en reposo tras un periodo de inactividad. ¡Agradecemos tu paciencia mientras se reactiva!

## Estructura del Proyecto

```text
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── docs/
│   ├── README.md
│   └── README-es.md
├── src/
│   ├── core/
│   │   ├── exceptions.py
│   │   └── security.py
│   ├── domains/
│   │   ├── tasks/
│   │   │   ├── models.py
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   └── users/
│   │       ├── models.py
│   │       ├── router.py
│   │       ├── schemas.py
│   │       └── service.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   └── models.py
├── tests/
│   ├── conftest.py
│   ├── test_tasks.py
│   └── test_users.py
├── .env
├── .env.example
├── alembic.ini
├── pyproject.toml
└── requirements.txt
```

El código fuente principal se encuentra en el directorio `src/`:
- `main.py`: Punto de entrada de la aplicación FastAPI, configuración de CORS y registro de rutas.
- `config.py`: Gestión de configuración y variables de entorno mediante Pydantic Settings.
- `database.py`: Conexión a la base de datos y creación de la sesión de SQLAlchemy.
- `dependencies.py`: Inyección de dependencias globales de FastAPI (ej., generador de sesión de base de datos `get_db` y autenticación JWT `get_current_user`).
- `models.py`: Módulo agregador que expone todos los modelos ORM de los dominios para las migraciones de Alembic e importaciones centralizadas.
- `core/`: Funcionalidades transversales del núcleo (`security.py` para JWT y hashing de contraseñas, `exceptions.py` para excepciones personalizadas).
- `domains/`: Contiene la lógica separada por dominios de negocio.
  - `users/`: Lógica (`models.py`, `schemas.py`, `router.py`, `service.py`) para usuarios y autenticación.
  - `tasks/`: Lógica (`models.py`, `schemas.py`, `router.py`, `service.py`) para la gestión de tareas.

Otros directorios y archivos clave:
- `alembic/` y `alembic.ini`: Configuración de migraciones de base de datos y scripts de versiones con Alembic.
- `tests/`: Pruebas automatizadas unitarias y de integración utilizando Pytest (`test_users.py`, `test_tasks.py`).
- `pyproject.toml` / `requirements.txt`: Gestión de dependencias del proyecto (compatible con `uv` y `pip` tradicional).
