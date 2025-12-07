def test_create_user_success(client):
    payload = {
    "username": "shamil",
    "email": "shamil@test.com",
    "password": "abcd"
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "shamil"
    assert data["email"] == "shamil@test.com"
    assert "password" not in data

def test_create_user_duplicate_email(client):
    payload = {
    "username": "user1",
    "email": "dup@test.com",
    "password": "abcd"
    }
    first = client.post("/users", json=payload)
    assert first.status_code == 200

    second = client.post("/users", json=payload)
    assert second.status_code == 400
    data = second.json()
    assert data["detail"] == "email already used"


def test_login_success(client):
    client.post(
    "/users",
    json={
    "username": "loginuser",
    "email": "login@test.com",
    "password": "abcd"
    },
    )
    response = client.post(
    "/login",
    data={
        "username": "loginuser",
        "password": "abcd"
    },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
def test_login_invalid_password(client):
    client.post(
    "/users",
    json={
    "username": "loginuser2",
    "email": "login2@test.com",
    "password": "abcd"
    },
    )
    response = client.post(
    "/login",
    data={
        "username": "loginuser2",
        "password": "wrong"
    },
)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "invalid credentials"
