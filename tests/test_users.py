
def test_create_user(client):
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
    payload = {
        "username": "testuser",
        "email": "testuser@test.com",
        "password": "testpassword"}

    response_firt = client.post("/users/register", json=payload)
    assert response_firt.status_code == 201

    response_duplicate = client.post("/users/register", json=payload)
    assert response_duplicate.status_code == 400
    assert response_duplicate.json() == {
        "detail": "Email and username already registered/Correo electonico y nombre de usuario ya registrados"}


def test_login_user(client):
    payload = {
        "username": "testuser",
        "email": "testuser@test.com",
        "password": "testpassword"}

    response_register = client.post("/users/register", json=payload)
    assert response_register.status_code == 201

    response_login = client.post("/users/login", data={"username": "testuser@test.com", "password": "testpassword"})
    assert response_login.status_code == 200
    assert response_login.json() == {"message": "Login successful/Inicio de sesión exitoso"}


def test_login_invalid_password(client):
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
    response_login = client.post("/users/login", data={"username": "nonexistent@test.com", "password": "anypassword"})
    assert response_login.status_code == 400
    assert response_login.json() == {
        "detail": "Incrorrect email or passwoard/Correo o Contraseña incorrecta"}


def test_get_current_user_unauthorized(client):
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated/No autenticado"}


def test_get_current_user_authorized(auth_client):
    response = auth_client.get("/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@test.com"
    assert "id" in data


def test_logout(auth_client):
    response_logout = auth_client.post("/users/logout")
    assert response_logout.status_code == 200
    assert response_logout.json() == {"message": "Sesión cerrada"}

    response_me = auth_client.get("/users/me")
    assert response_me.status_code == 401
    assert response_me.json() == {"detail": "Not authenticated/No autenticado"}
