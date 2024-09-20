import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="function")
def user_token(client, db):
    """
    Fixture to register and log in a user, returning the access token for authentication.
    """
    # Register a new user
    register_response = client.post("/api/v1/auth/register", json={
        "username": "user",
        "email": "user@example.com",
        "password": "userpassword",
        "role": "user"
    })
    print(f"User Registration Response: {register_response.status_code}")
    print(f"User Registration Content: {register_response.content}")
    
    # Log in the user to get an access token
    login_response = client.post("/api/v1/auth/login", json={
        "username": "user",
        "password": "userpassword"
    })
    print(f"User Login Response: {login_response.status_code}")
    print(f"User Login Content: {login_response.content}")
    
    return login_response.json()["access_token"]

@pytest.fixture(scope="function")
def admin_token(client, db):
    """
    Fixture to register and log in an admin, returning the access token for authentication.
    """
    # Register a new admin
    register_response = client.post("/api/v1/auth/register", json={
        "username": "admin",
        "email": "admin@example.com",
        "password": "adminpassword",
        "role": "admin"
    })
    print(f"Admin Registration Response: {register_response.status_code}")
    print(f"Admin Registration Content: {register_response.content}")
    
    # Log in the admin to get an access token
    login_response = client.post("/api/v1/auth/login", json={
        "username": "admin",
        "password": "adminpassword"
    })
    print(f"Admin Login Response: {login_response.status_code}")
    print(f"Admin Login Content: {login_response.content}")
    
    return login_response.json()["access_token"]

def test_create_tool_as_admin(client, admin_token, db):
    """
    Test case to verify that an admin can create a new tool.
    """
    response = client.post(
        "/api/v1/tools/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "Hammer", "description": "A tool for hammering nails", "category": "Hand Tools"}
    )
    print(f"Create tool response: {response.status_code}")
    print(f"Response content: {response.content}")
    assert response.status_code == 201
    assert "id" in response.json()

def test_create_tool_as_user(client, user_token, db):
    """
    Test case to verify that a regular user cannot create a new tool.
    """
    response = client.post(
        "/api/v1/tools/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"name": "Screwdriver", "description": "A tool for driving screws", "category": "Hand Tools"}
    )
    print(f"Create tool as user response: {response.status_code}")
    print(f"Response content: {response.content}")
    assert response.status_code == 403

def test_read_tools_as_user(client, user_token, db):
    """
    Test case to verify that a regular user can read tools.
    """
    response = client.get(
        "/api/v1/tools/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    print(f"Read tools as user response: {response.status_code}")
    print(f"Response content: {response.content}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_tools_as_admin(client, admin_token, db):
    """
    Test case to verify that an admin can read tools.
    """
    response = client.get(
        "/api/v1/tools/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"Read tools as admin response: {response.status_code}")
    print(f"Response content: {response.content}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_sample_tools_as_admin(client, admin_token, db):
    """
    Test case to verify that an admin can create sample tools.
    """
    response = client.post(
        "/api/v1/tools/sample",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"Create sample tools response: {response.status_code}")
    print(f"Response content: {response.content}")
    assert response.status_code == 201

def test_create_sample_tools_as_user(client, user_token, db):
    """
    Test case to verify that a regular user cannot create sample tools.
    """
    response = client.post(
        "/api/v1/tools/sample",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    print(f"Create sample tools as user response: {response.status_code}")
    print(f"Response content: {response.content}")
    assert response.status_code == 403

def test_update_tool_as_admin(client, admin_token, db):
    """
    Test case to verify that an admin can update a tool.
    """
    # First, create a tool
    create_response = client.post(
        "/api/v1/tools/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "Wrench", "description": "A tool for tightening bolts", "category": "Hand Tools"}
    )
    print(f"Create tool response: {create_response.status_code}")
    print(f"Response content: {create_response.content}")
    tool_id = create_response.json()["id"]

    # Then, update the tool
    update_response = client.put(
        f"/api/v1/tools/{tool_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "Adjustable Wrench", "description": "An adjustable tool for tightening bolts", "category": "Hand Tools"}
    )
    print(f"Update tool response: {update_response.status_code}")
    print(f"Response content: {update_response.content}")
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Adjustable Wrench"

def test_update_tool_as_user(client, user_token, admin_token, db):
    """
    Test case to verify that a regular user cannot update a tool created by an admin.
    """
    # First, create a tool as admin
    create_response = client.post(
        "/api/v1/tools/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "Pliers", "description": "A tool for gripping objects", "category": "Hand Tools"}
    )
    print(f"Create tool response: {create_response.status_code}")
    print(f"Response content: {create_response.content}")
    tool_id = create_response.json()["id"]

    # Then, try to update the tool as user
    update_response = client.put(
        f"/api/v1/tools/{tool_id}",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"name": "Needle-nose Pliers", "description": "A tool for gripping small objects", "category": "Hand Tools"}
    )
    print(f"Update tool as user response: {update_response.status_code}")
    print(f"Response content: {update_response.content}")
    assert update_response.status_code == 403

def test_delete_tool_as_admin(client, admin_token, db):
    """
    Test case to verify that an admin can delete a tool.
    """
    # First, create a tool
    create_response = client.post(
        "/api/v1/tools/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "Saw", "description": "A tool for cutting wood", "category": "Hand Tools"}
    )
    print(f"Create tool response: {create_response.status_code}")
    print(f"Response content: {create_response.content}")
    tool_id = create_response.json()["id"]

    # Then, delete the tool
    delete_response = client.delete(
        f"/api/v1/tools/{tool_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"Delete tool response: {delete_response.status_code}")
    print(f"Response content: {delete_response.content}")
    assert delete_response.status_code == 204

def test_delete_tool_as_user(client, user_token, admin_token, db):
    """
    Test case to verify that a regular user cannot delete a tool created by an admin.
    """
    # First, create a tool as admin
    create_response = client.post(
        "/api/v1/tools/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "Drill", "description": "A tool for making holes", "category": "Power Tools"}
    )
    print(f"Create tool response: {create_response.status_code}")
    print(f"Response content: {create_response.content}")
    tool_id = create_response.json()["id"]

    # Then, try to delete the tool as user
    delete_response = client.delete(
        f"/api/v1/tools/{tool_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    print(f"Delete tool as user response: {delete_response.status_code}")
    print(f"Response content: {delete_response.content}")
    assert delete_response.status_code == 403
