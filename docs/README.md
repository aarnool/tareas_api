[🇬🇧 English](README.md)    [🇪🇸 Spanish](README-es.md)    
# Simple Tasks API (Task Management API)

This is a RESTful API built with **FastAPI** and **SQLAlchemy** for managing users and tasks.

## Technologies Used

- **FastAPI**: Fast web framework for building APIs with Python.
- **SQLAlchemy**: ORM (Object Relational Mapper) for database interaction.
- **PyMySQL**: Python connector for synchronous MySQL databases.
- **Pydantic**: Data validation and settings management.

## Installation and Configuration

1. **Prerequisites**:
   Make sure you have Python 3.14 or higher installed.

2. **Virtual Environment**:
   It is recommended to use a virtual environment and manage dependencies using the `pyproject.toml` file (this project uses `uv`) or `requirements.txt` (for standard `pip`).

3. **Run the application**:
   You can start the server locally with the following command (thanks to `fastapi-cli`):
   ```bash
   fastapi dev src/main.py
   ```
   The API will be available at `http://localhost:8000`. 
   You can access the interactive documentation (Swagger UI) at `http://localhost:8000/docs`.

## API Endpoints

### Root
- **`GET /`**: Health check root endpoint to verify that the API is running.

### Users (Authentication & Management)
- **`POST /users/register`**: Registers a new user account (validates unique username and email, hashes password).
- **`POST /users/login`**: Authenticates a user with OAuth2 credentials (email/username and password) and sets a secure HTTP-only JWT cookie (`auth_token`).
- **`GET /users/me`**: Retrieves the profile information of the currently authenticated user (requires valid `auth_token` cookie).
- **`POST /users/logout`**: Logs out the user by clearing the authentication cookie.

### Tasks (User Isolated)
- **`POST /tasks`**: Creates a new task associated with the authenticated user (default status `pending`, default priority `medium`).
- **`GET /tasks`**: Retrieves a paginated list of all tasks belonging to the authenticated user (supports `start` and `limit` parameters).
- **`PATCH /tasks/{task_id}`**: Partially or totally updates a task's details by ID (restricted to the task owner).
- **`DELETE /tasks/{task_id}`**: Deletes a task by ID (restricted to the task owner).

## Project Structure

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

The main source code is located in the `src/` directory:
- `main.py`: Entry point of the FastAPI application, CORS setup, and router registration.
- `config.py`: Configuration and environment variables management using Pydantic Settings.
- `database.py`: Database connection and SQLAlchemy session creation.
- `dependencies.py`: Global FastAPI dependency injection (e.g., database session generator `get_db` and JWT authentication `get_current_user`).
- `models.py`: Aggregator module that exposes all domain ORM models for Alembic migrations and centralized imports.
- `core/`: Cross-cutting core functionalities (`security.py` for JWT and password hashing, `exceptions.py` for custom errors).
- `domains/`: Contains the logic separated by business domains.
  - `users/`: Logic (`models.py`, `schemas.py`, `router.py`, `service.py`) for user management and authentication.
  - `tasks/`: Logic (`models.py`, `schemas.py`, `router.py`, `service.py`) for task management.

Other key directories and files:
- `alembic/` & `alembic.ini`: Database migrations configuration and version scripts.
- `tests/`: Automated unit and integration tests using Pytest (`test_users.py`, `test_tasks.py`).
- `pyproject.toml` / `requirements.txt`: Project dependency management (compatible with both `uv` and standard `pip`).
