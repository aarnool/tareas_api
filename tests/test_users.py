
"""Módulo de pruebas de integración para los endpoints de autenticación y usuarios."""


def test_create_user(client):
    """Verifica el registro exitoso de un nuevo usuario devolviendo código 201."""
    payload = {
        "username": "testuser",
        "email": "testuser@test.com",
        "password": "testpassword"}

    response = client.post("/users/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@test.com"
    assert "id" in data


def test_create_user_duplicate(client):
    """Comprueba que se rechaza el registro si el correo o usuario ya existen (400 Bad Request)."""
    payload = {
        "username": "testuser",
        "email": "testuser@test.com",
        "password": "testpassword"}

    response = client.post("/users/register", json=payload)
    assert response.status_code == 201

    # Intento de segundo registro con el mismo username
    payload.update({"email": "testuser2@test.com"})
    response_duplicate_username = client.post("/users/register", json=payload)
    assert response_duplicate_username.status_code == 400
    assert response_duplicate_username.json() == {
        "detail": "Email and username already registered/Correo electonico y nombre de usuario ya registrados"}
    # Intento de segundo registro con el mismo email
    payload.update({"username": "testuser2", "email": "testuser@test.com"})
    response_duplicate_email = client.post("/users/register", json=payload)
    assert response_duplicate_email.status_code == 400
    assert response_duplicate_email.json() == {
        "detail": "Email and username already registered/Correo electonico y nombre de usuario ya registrados"}


def test_login_user(client):
    """Prueba el inicio de sesión exitoso obteniendo la cookie JWT y respuesta 200."""
    payload = {
        "username": "testuser",
        "email": "testuser@test.com",
        "password": "testpassword"}

    response_register = client.post("/users/register", json=payload)
    assert response_register.status_code == 201

    # OAuth2 usa el campo 'username' en el formulario para pasar el correo del usuario
    response_login = client.post("/users/login", data={"username": "testuser@test.com", "password": "testpassword"})
    assert response_login.status_code == 200
    assert response_login.json() == {"message": "Login successful/Inicio de sesión exitoso"}


def test_login_invalid_password(client):
    """Asegura que una contraseña incorrecta devuelva el error de credenciales 400."""
    payload = {
        "username": "testuser",
        "email": "testuser@test.com",
        "password": "testpassword"}

    client.post("/users/register", json=payload)
    response_login = client.post("/users/login", data={"username": "testuser@test.com", "password": "wrongpassword"})
    assert response_login.status_code == 400
    assert response_login.json() == {
        "detail": "Incrorrect email or passwoard/Correo o Contraseña incorrecta"}


def test_login_nonexistent_email(client):
    """Verifica el error 400 al intentar loguearse con un correo no registrado."""
    response_login = client.post("/users/login", data={"username": "nonexistent@test.com", "password": "anypassword"})
    assert response_login.status_code == 400
    assert response_login.json() == {
        "detail": "Incrorrect email or passwoard/Correo o Contraseña incorrecta"}


def test_get_current_user_unauthorized(client):
    """Valida que una petición sin cookie de autenticación sea denegada (401 Unauthorized)."""
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated/No autenticado"}


def test_get_current_user_authorized(auth_client):
    """Comprueba que el cliente autenticado puede recuperar su perfil correctamente."""
    response = auth_client.get("/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@test.com"
    assert "id" in data


def test_logout(auth_client):
    """Verifica que el cierre de sesión invalide la cookie y revoque el acceso a `/users/me`."""
    response_logout = auth_client.post("/users/logout")
    assert response_logout.status_code == 200
    assert response_logout.json() == {"message": "Sesión cerrada"}

    # Después del logout, las peticiones posteriores deben fallar por falta de sesión
    response_me = auth_client.get("/users/me")
    assert response_me.status_code == 401
    assert response_me.json() == {"detail": "Not authenticated/No autenticado"}

