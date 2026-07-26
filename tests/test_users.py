
def test_create_user(client):
    payload = {
        "username": "testuser",
        "email": "testuser@test.com",
        "password": "testpassword"}

    response =  client.post("/users/register", json=payload)
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
