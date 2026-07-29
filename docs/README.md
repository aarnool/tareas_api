[🇬🇧 English](README.md)    [🇪🇸 Spanish](README-es.md)    
# Simple Tasks API (Task Management API)

This is a RESTful API built with **FastAPI** and **SQLAlchemy** for managing users and tasks.

## Technologies Used

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Fast web framework for building APIs with Python.
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) - Object Relational Mapper for robust database interactions.
- **Database**: [PyMySQL](https://pymysql.readthedocs.io/) - Python connector for synchronous MySQL databases.
- **Validation**: [Pydantic](https://docs.pydantic.dev/) - Data validation and settings management.
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/) - Lightweight database migration tool.

---

## ⚙️ Installation and Configuration

### 1. Prerequisites
Make sure you have **Python 3.14 or higher** installed.

2. **Virtual Environment**:
   It is recommended to use a virtual environment and manage dependencies using the `pyproject.toml` file (this project uses `uv`) or `requirements.txt` (for standard `pip`).

3. **Run the application**:
   You can start the server locally with the following command (thanks to `fastapi-cli`):
   ```bash
   fastapi dev src/main.py
   ```
   The API will be available at `http://localhost:8000`. 
   You can access the interactive documentation (Swagger UI) without cloning or running in `https://tareas-api-lc94.onrender.com/docs`.

> **Important Note:** If the documentation takes a few seconds to load initially, it is because the backend is deployed on a free Render instance that goes into sleep mode after a period of inactivity. We appreciate your patience while it wakes up!
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

## 🏛️ Diagrams and Architecture

### Physical Model
![Physical Model](public/physical_model.png)

### Sequence Diagram: JWT Token Creation
![Sequence Diagram](public/sequence_diagram.png)

### Flowchart: Account Creation
![Flowchart 1](public/flowchart(1).png)

### Protected Endpoints (Requires JWT)
![Flowchart 2](public/flowchart(2).png)

## Screenshots / Examples

### API Documentation (Swagger UI)
![API Documentation](public/doc.png)

### Frontend Use Case Example
You can test the live frontend application here: **[Frontend Demonstration](https://frontend-seven-livid-1rwmj8gd6q.vercel.app/)**

![Frontend Interface](public/ejem.png)

> **Important Note:** If the frontend takes a few seconds to respond on the initial load, it is because the backend is deployed on a free instance on Render, which spins down after a period of inactivity. We appreciate your patience while it spins back up!

## 📂 Project Structure

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
