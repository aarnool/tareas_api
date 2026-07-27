"""Módulo de pruebas de integración para los endpoints de gestión de tareas y aislamiento por usuario."""


def test_create_task_unauthorized(client):
    """Verifica que no se pueda crear una tarea sin estar autenticado (401 Unauthorized)."""
    response = client.post("/tasks", json={"title": "Test Task"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated/No autenticado"}


def test_create_task(auth_client):
    """Comprueba la creación exitosa de una tarea con todos sus atributos (201 Created)."""
    payload = {
        "title": "Aprender FastAPI",
        "description": "Estudiar la documentación y escribir tests",
        "status": "in_progress",
        "priority": "high"
    }
    response = auth_client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Aprender FastAPI"
    assert data["description"] == "Estudiar la documentación y escribir tests"
    assert data["status"] == "in_progress"
    assert data["priority"] == "high"
    assert "id" in data
    assert "created_at" in data
    assert data["updated_at"] is None


def test_create_task_default_values(auth_client):
    """Asegura que al omitir campos opcionales se apliquen los valores por defecto (`pending` y `medium`)."""
    payload = {
        "title": "Tarea sencilla sin descripción"
    }
    response = auth_client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Tarea sencilla sin descripción"
    assert data["description"] is None
    assert data["status"] == "pending"
    assert data["priority"] == "medium"


def test_create_task_invalid_status(auth_client):
    """Valida el error 422 si se envía un valor de estado que no pertenece al enum permitido."""
    payload = {
        "title": "Tarea con estado inválido",
        "status": "estado_invalido"
    }
    response = auth_client.post("/tasks", json=payload)
    assert response.status_code == 422


def test_get_all_tasks_unauthorized(client):
    """Verifica que el listado de tareas esté protegido contra clientes no autenticados."""
    response = client.get("/tasks")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated/No autenticado"}


def test_get_all_tasks_empty(auth_client):
    """Comprueba que un usuario nuevo reciba una lista vacía de tareas con código 200."""
    response = auth_client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_tasks(auth_client):
    """Verifica la recuperación correcta de múltiples tareas creadas por el usuario autenticado."""
    auth_client.post("/tasks", json={"title": "Tarea 1"})
    auth_client.post("/tasks", json={"title": "Tarea 2"})

    response = auth_client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Tarea 1"
    assert data[1]["title"] == "Tarea 2"


def test_get_all_tasks_pagination(auth_client):
    """Valida el funcionamiento de la paginación mediante los parámetros de consulta `start` y `limit`."""
    auth_client.post("/tasks", json={"title": "Tarea A"})
    auth_client.post("/tasks", json={"title": "Tarea B"})
    auth_client.post("/tasks", json={"title": "Tarea C"})

    # Salta el primer elemento (index 0) y limita la respuesta a un solo registro
    response = auth_client.get("/tasks", params={"start": 1, "limit": 1})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Tarea B"


def test_update_task_unauthorized(client):
    """Asegura que un cliente anónimo no pueda modificar una tarea por ID (401 Unauthorized)."""
    response = client.patch("/tasks/1", json={"title": "Actualizado"})
    assert response.status_code == 401


def test_update_task(auth_client):
    """Prueba la modificación total de los campos de una tarea existente del usuario (200 OK)."""
    create_response = auth_client.post("/tasks", json={"title": "Original"})
    task_id = create_response.json()["id"]

    update_payload = {
        "title": "Modificado",
        "status": "done",
        "priority": "low"
    }
    response = auth_client.patch(f"/tasks/{task_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Modificado"
    assert data["status"] == "done"
    assert data["priority"] == "low"
    assert data["updated_at"] is not None


def test_update_task_partial(auth_client):
    """Comprueba la actualización parcial alterando solo el estado sin perder título ni descripción."""
    create_response = auth_client.post("/tasks", json={"title": "Original", "description": "Desc"})
    task_id = create_response.json()["id"]

    response = auth_client.patch(f"/tasks/{task_id}", json={"status": "in_progress"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Original"
    assert data["description"] == "Desc"
    assert data["status"] == "in_progress"


def test_update_task_not_found(auth_client):
    """Verifica el error 404 al intentar actualizar una tarea con un ID inexistente en la base de datos."""
    response = auth_client.patch("/tasks/9999", json={"title": "Inexistente"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found/Tarea no encontrada"}


def test_delete_task_unauthorized(client):
    """Asegura que un usuario sin sesión no pueda eliminar tareas (401 Unauthorized)."""
    response = client.delete("/tasks/1")
    assert response.status_code == 401


def test_delete_task(auth_client):
    """Comprueba la eliminación exitosa de una tarea devolviendo código HTTP 204 sin contenido."""
    create_response = auth_client.post("/tasks", json={"title": "Para borrar"})
    task_id = create_response.json()["id"]

    delete_response = auth_client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    # Confirma que la tarea ya no aparezca en el listado del usuario
    get_response = auth_client.get("/tasks")
    assert len(get_response.json()) == 0


def test_delete_task_not_found(auth_client):
    """Verifica que intentar eliminar un ID inexistente devuelva error 404."""
    response = auth_client.delete("/tasks/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found/Tarea no encontrada"}


def test_delete_task_twice(auth_client):
    """Asegura que un segundo intento de eliminar la misma tarea genere error 404 Not Found."""
    create_response = auth_client.post("/tasks", json={"title": "Para borrar doble"})
    task_id = create_response.json()["id"]

    auth_client.delete(f"/tasks/{task_id}")
    second_delete = auth_client.delete(f"/tasks/{task_id}")
    assert second_delete.status_code == 404
    assert second_delete.json() == {"detail": "Task not found/Tarea no encontrada"}


def test_tasks_user_isolation(client):
    """Garantiza el estricto aislamiento de datos entre usuarios impidiendo lecturas o modificaciones cruzadas."""
    # Registro e inicio de sesión del Usuario 1
    client.post("/users/register", json={"username": "user1", "email": "u1@test.com", "password": "pass"})
    client.post("/users/login", data={"username": "u1@test.com", "password": "pass"})
    res1 = client.post("/tasks", json={"title": "Tarea de Usuario 1"})
    task_id_u1 = res1.json()["id"]

    # Cierre de sesión del Usuario 1
    client.post("/users/logout")

    # Registro e inicio de sesión del Usuario 2
    client.post("/users/register", json={"username": "user2", "email": "u2@test.com", "password": "pass"})
    client.post("/users/login", data={"username": "u2@test.com", "password": "pass"})
    client.post("/tasks", json={"title": "Tarea de Usuario 2"})

    # El Usuario 2 solo debe ver y acceder a su propia tarea
    get_res = client.get("/tasks")
    assert get_res.status_code == 200
    tasks_u2 = get_res.json()
    assert len(tasks_u2) == 1
    assert tasks_u2[0]["title"] == "Tarea de Usuario 2"

    # El Usuario 2 intenta modificar la tarea del Usuario 1 -> debe ser rechazado con 404
    patch_res = client.patch(f"/tasks/{task_id_u1}", json={"title": "Hacked"})
    assert patch_res.status_code == 404

    # El Usuario 2 intenta eliminar la tarea del Usuario 1 -> debe ser rechazado con 404
    delete_res = client.delete(f"/tasks/{task_id_u1}")
    assert delete_res.status_code == 404

