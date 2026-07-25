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
   Se recomienda usar un entorno virtual y administrar las dependencias utilizando el archivo `pyproject.toml` (este proyecto utiliza `uv`).

3. **Ejecutar la aplicación**:
   Puedes iniciar el servidor localmente con el siguiente comando (gracias a `fastapi-cli`):
   ```bash
   fastapi dev src/main.py
   ```
   La API estará disponible en `http://localhost:8000`. 
   Puedes acceder a la documentación interactiva (Swagger UI) en `http://localhost:8000/docs`.

## Endpoints de la API

### Usuarios (Users)
- **`POST /users`**: Crea un nuevo usuario.
- **`GET /users`**: Obtiene la lista de todos los usuarios (admite paginación con `start` y `limit`).
- **`GET /users/{user_id}`**: Obtiene un usuario específico por su ID único.
- **`PATCH /users/{user_id}`**: Actualiza parcialmente la información de un usuario.
- **`DELETE /users/{user_id}`**: Elimina un usuario por su ID.

### Tareas (Tasks)
- **`POST /tasks`**: Crea una nueva tarea asociada a un usuario.
- **`GET /tasks`**: Obtiene una lista de todas las tareas (admite paginación).
- **`GET /tasks/{task_id}`**: Obtiene una tarea específica por su ID.
- **`PATCH /tasks/{task_id}`**: Actualiza los detalles de una tarea.
- **`DELETE /tasks/{task_id}`**: Elimina una tarea por su ID.

## Estructura del Proyecto

```text
├── src/
│   ├── core/
│   ├── domains/
│   │   ├── tasks/
│   │   │   ├── dependencies.py
│   │   │   ├── models.py
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   └── users/
│   │       ├── dependencies.py
│   │       ├── models.py
│   │       ├── router.py
│   │       ├── schemas.py
│   │       └── service.py
│   ├── config.py
│   ├── database.py
│   └── main.py
├── docs/
│   ├── README.md
│   └── README-en.md
├── .env
└── pyproject.toml
```

El código fuente principal se encuentra en el directorio `src/`:
- `main.py`: Punto de entrada de la aplicación FastAPI.
- `database.py` / `config.py`: Configuración y conexión a la base de datos.
- `domains/`: Contiene la lógica separada por dominios de negocio.
  - `users/`: Lógica (modelos, esquemas, endpoints) para los usuarios.
  - `tasks/`: Lógica (modelos, esquemas, endpoints) para las tareas.
