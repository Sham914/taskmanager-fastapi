def create_user_and_login(client):
    client.post(
    "/users",
    json={
    "username": "taskuser",
    "email": "task@test.com",
    "password": "abcd"
    },
    )
    response = client.post(
    "/login",
    data={
        "username": "taskuser",
        "password": "abcd"
    },
)
    token = response.json()["access_token"]
    return token

def test_create_task_requires_auth(client):
    payload = {
    "title": "No auth task",
    "description": "Should fail",
    "priority": 1
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 401

def test_create_task_with_auth(client):
    token = create_user_and_login(client)
    payload = {
    "title": "First task",
    "description": "Protected create",
    "priority": 1
}

    response = client.post(
        "/tasks",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "First task"
    assert data["completed"] is False

def test_list_tasks_with_auth(client):
    token = create_user_and_login(client)
    client.post(
    "/tasks",
    json={
        "title": "Task one",
        "description": "List test",
        "priority": 1
    },
    headers={"Authorization": f"Bearer {token}"}
)

    response = client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "Task one"

