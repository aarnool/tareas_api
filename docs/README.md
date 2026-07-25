TRADUCIR:   [🇬🇧 English](README.md)    [🇪🇸 Spanish](README-es.md)    
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
   It is recommended to use a virtual environment and manage dependencies using the `pyproject.toml` file (this project uses `uv`).

3. **Run the application**:
   You can start the server locally with the following command (thanks to `fastapi-cli`):
   ```bash
   fastapi dev src/main.py
   ```
   The API will be available at `http://localhost:8000`. 
   You can access the interactive documentation (Swagger UI) at `http://localhost:8000/docs`.

## API Endpoints

### Users
- **`POST /users`**: Creates a new user.
- **`GET /users`**: Gets the list of all users (supports pagination with `start` and `limit`).
- **`GET /users/{user_id}`**: Gets a specific user by their unique ID.
- **`PATCH /users/{user_id}`**: Partially updates a user's information.
- **`DELETE /users/{user_id}`**: Deletes a user by their ID.

### Tasks
- **`POST /tasks`**: Creates a new task associated with a user.
- **`GET /tasks`**: Gets a list of all tasks (supports pagination).
- **`GET /tasks/{task_id}`**: Gets a specific task by its ID.
- **`PATCH /tasks/{task_id}`**: Updates a task's details.
- **`DELETE /tasks/{task_id}`**: Deletes a task by its ID.

## Project Structure

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

The main source code is located in the `src/` directory:
- `main.py`: Entry point of the FastAPI application.
- `database.py` / `config.py`: Database configuration and connection.
- `domains/`: Contains the logic separated by business domains.
  - `users/`: Logic (models, schemas, endpoints) for users.
  - `tasks/`: Logic (models, schemas, endpoints) for tasks.
