import pytest

@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers"""
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_todo(client, auth_headers):
    """Test creating a todo"""
    response = client.post("/todos", json={
        "title": "Test Todo",
        "description": "This is a test todo"
    }, headers=auth_headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["completed"] == False

def test_get_todos(client, auth_headers):
    """Test getting todos"""
    # Create a todo first
    client.post("/todos", json={
        "title": "Test Todo",
        "description": "Test description"
    }, headers=auth_headers)
    
    # Get todos
    response = client.get("/todos", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["todos"]) == 1
    assert data["total"] == 1

def test_update_todo(client, auth_headers):
    """Test updating a todo"""
    # Create todo
    create_response = client.post("/todos", json={
        "title": "Original Title",
        "description": "Original description"
    }, headers=auth_headers)
    todo_id = create_response.json()["id"]
    
    # Update todo
    response = client.put(f"/todos/{todo_id}", json={
        "title": "Updated Title",
        "completed": True
    }, headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["completed"] == True

def test_delete_todo(client, auth_headers):
    """Test deleting a todo"""
    # Create todo
    create_response = client.post("/todos", json={
        "title": "To be deleted",
        "description": "This will be deleted"
    }, headers=auth_headers)
    todo_id = create_response.json()["id"]
    
    # Delete todo
    response = client.delete(f"/todos/{todo_id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Verify deletion
    get_response = client.get(f"/todos/{todo_id}", headers=auth_headers)
    assert get_response.status_code == 404