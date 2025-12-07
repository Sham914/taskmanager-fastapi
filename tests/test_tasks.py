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

def test_tasks_Are_owned_by_user(client):
    token1=create_user_and_login(client)
    client.post(
    "/tasks",
    json={
        "title": "User1 task",
        "description": "belongs to user1",
        "priority": 1
    },
    headers={"Authorization": f"Bearer {token1}"}
)

    # create second user
    client.post(
        "/users",
        json={
            "username": "user2",
            "email": "user2@test.com",
            "password": "abcd"
        },
    )
    response_login2 = client.post(
        "/login",
        data={
            "username": "user2",
            "password": "abcd"
        },
    )
    token2 = response_login2.json()["access_token"]

    response = client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {token2}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data == []
    
def test_update_task(client):
    token=create_user_and_login(client)
    create_resp = client.post(
    "/tasks",
    json={
        "title": "Old title",
        "description": "Old desc",
        "priority": 1
    },
    headers={"Authorization": f"Bearer {token}"}
)
    task_id = create_resp.json()["id"]

    update_resp = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "New title",
            "description": "New desc",
            "priority": 2
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert update_resp.status_code == 200
    data = update_resp.json()
    assert data["title"] == "New title"
    assert data["priority"] == 2

def test_delete_task(client):
    token=create_user_and_login(client)
    create_resp = client.post(
    "/tasks",
    json={
        "title": "Delete me",
        "description": "To delete",
        "priority": 1
    },
    headers={"Authorization": f"Bearer {token}"}
)
    task_id = create_resp.json()["id"]

    delete_resp = client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert delete_resp.status_code == 204

    list_resp = client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    tasks = list_resp.json()
    assert len(tasks) == 0
