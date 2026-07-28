def test_greeting_limit(client):
    """Prueba la ruta raíz para asegurarse de que devuelve un saludo y un código de estado 200."""
    for _ in range(5):  # Límite de 5/minuto
        response = client.get("/")
        assert response.status_code == 200

    response = client.get("/")
    assert response.status_code == 429

def test_register_limit(client):
    """Prueba el límite de 10/hora en /users/register"""
    for i in range(10): #Limite de 10/hora
        response = client.post("/users/register", json={
            "username": f"user_limit_{i}", 
            "email": f"ulimit{i}@test.com", 
            "password": "123"
        })
        assert response.status_code == 201 
        
    response = client.post("/users/register", json={
        "username": "user_limit_10", 
        "email": "ulimit10@test.com", 
        "password": "123"
    })
    assert response.status_code == 429

def test_login_limit(client):
    """Prueba el límite de 5/minuto en /users/login"""
    client.post("/users/register", json={
        "username": "fakeuser", 
        "email": "fake@test.com",
        "password": "123"
    })
    
    for _ in range(5):
        response = client.post("/users/login", data={"username": "fake@test.com", "password": "123"})
        assert response.status_code == 200
        client.post("/users/logout")  # Cierra sesión para permitir el siguiente intento de inicio de sesión
        
    response = client.post("/users/login", data={"username": "fake@test.com", "password": "123"})
    assert response.status_code == 429

def test_get_user_me_limit(auth_client):
    """Prueba el límite de 10/minuto en /users/me"""
    for _ in range(10):
        response = auth_client.get("/users/me")
        assert response.status_code == 200
        
    response = auth_client.get("/users/me")
    assert response.status_code == 429

def test_create_task_limit(auth_client):
    """Prueba el límite de 10/minute en POST /tasks"""
    for _ in range(10):
        response = auth_client.post("/tasks", json={"title": "Test"})
        assert response.status_code == 201
        
    response = auth_client.post("/tasks", json={"title": "Test"})
    assert response.status_code == 429

def test_get_all_tasks_limit(auth_client):
    """Prueba el límite de 10/minute en GET /tasks"""
    for _ in range(10):
        response = auth_client.get("/tasks")
        assert response.status_code == 200
        
    response = auth_client.get("/tasks")
    assert response.status_code == 429

def test_update_task_limit(auth_client):
    """Prueba el límite de 10/minute en PATCH /tasks/{task_id}"""
    # Crear tarea primero para que exista
    resp = auth_client.post("/tasks", json={"title": "Original"})
    task_id = resp.json()["id"]

    for _ in range(10):
        response = auth_client.patch(f"/tasks/{task_id}", json={"title": "Update"})
        assert response.status_code == 200
        
    response = auth_client.patch(f"/tasks/{task_id}", json={"title": "Update"})
    assert response.status_code == 429

def test_delete_task_limit(auth_client):
    """Prueba el límite de 10/minute en DELETE /tasks/{task_id}"""
    resp = auth_client.post("/tasks", json={"title": "Borrar"})
    task_id = resp.json()["id"]

    for _ in range(10):
        # Primera vez da 204, las siguientes 404, pero todas cuentan para el límite
        response = auth_client.delete(f"/tasks/{task_id}")
        assert response.status_code in (204, 404)
        
    response = auth_client.delete(f"/tasks/{task_id}")
    assert response.status_code == 429
