import pytest
import json
from rest_framework.test import APIClient
from datetime import date, timedelta 

# ✅ Fixture to create a reusable API client
@pytest.fixture
def client():
    return APIClient()

# -----------------------------
# TEST 1: Create a task
# -----------------------------
def test_create_task(client):
    response = client.post("/api/tasks/", {
        "title": "Test Task",
        "description": "Testing",
        "due_date": "2025-08-09",
        "status": "Pending"
    }, format="json")

    data = json.loads(response.content)  # Parse JSON
    assert response.status_code == 201  # Created successfully

    # ✅ If API returns full task object
    if "title" in data:
        assert data["title"] == "Test Task"
    # ✅ If API returns only message
    elif "message" in data:
        assert "created" in data["message"].lower()
    else:
        pytest.fail(f"Unexpected response format: {data}")


# -----------------------------
# TEST 2: Get all tasks
# -----------------------------
def test_get_tasks(client):
    response = client.get("/api/tasks/")
    data = json.loads(response.content)

    assert response.status_code == 200
    assert isinstance(data, list)  # Should return a list

# -----------------------------
# TEST 3: Update a task
# -----------------------------
def test_update_task(client):
    # Step 1: Create a new task
    create = client.post("/api/tasks/", {
        "title": "Update Test",
        "description": "Before update",
        "due_date": "2025-08-09",
        "status": "Pending"
    }, format="json")

    create_data = json.loads(create.content)
    assert create.status_code == 201

    # ✅ Try to get ID directly, otherwise fetch tasks list
    if "id" in create_data:
        task_id = create_data["id"]
    else:
        # Fetch latest task from GET endpoint
        get_tasks = client.get("/api/tasks/")
        tasks_list = json.loads(get_tasks.content)
        assert isinstance(tasks_list, list) and len(tasks_list) > 0
        task_id = tasks_list[-1]["id"]

    # Step 2: Update the task
    update = client.put(f"/api/tasks/{task_id}/", {
        "title": "Update Test",
        "description": "After update",
        "due_date": "2025-08-09",
        "status": "Completed"
    }, format="json")

    update_data = json.loads(update.content)

    # Step 3: Assertions
    assert update.status_code == 200
    if "status" in update_data:
        assert update_data["status"] == "Completed"
    elif "message" in update_data:
        assert "updated" in update_data["message"].lower()

# -----------------------------
# Helper function to create task
# -----------------------------
def create_sample_task(client, title="Sample Task"):
    response = client.post("/api/tasks/", {
        "title": title,
        "description": "Description",
        "due_date": "2025-08-09",
        "status": "Pending"
    }, format="json")
    assert response.status_code == 201
    return json.loads(response.content)



# -----------------------------
# TEST 4: Create a task
# -----------------------------
def test_create_task1(client):
    data = create_sample_task(client)
    assert data["message"] == "Task created successfully."



