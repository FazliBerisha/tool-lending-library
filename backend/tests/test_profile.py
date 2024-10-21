"""
This module contains tests for user profile-related functionality.
It includes tests for retrieving, updating, and managing user profiles,
as well as testing authorization and access control for different user roles.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="function")
def user_token(client, db):
    # Register a new user with profile fields
    register_response = client.post("/api/v1/auth/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
        "role": "user",
        "full_name": "Test User",
        "bio": "Test user bio",
        "location": "Test City"
    })
    assert register_response.status_code == 201, f"User registration failed: {register_response.content}"
    
    # Log in the user to get an access token
    login_response = client.post("/api/v1/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert login_response.status_code == 200, f"User login failed: {login_response.content}"
    
    return login_response.json()["access_token"]

@pytest.fixture(scope="function")
def admin_token(client, db):
    # Register a new admin with profile fields
    register_response = client.post("/api/v1/auth/register", json={
        "username": "testadmin",
        "email": "testadmin@example.com",
        "password": "adminpassword",
        "role": "admin",
        "full_name": "Test Admin",
        "bio": "Test admin bio",
        "location": "Admin City"
    })
    assert register_response.status_code == 201, f"Admin registration failed: {register_response.content}"
    
    # Log in the admin to get an access token
    login_response = client.post("/api/v1/auth/login", json={
        "username": "testadmin",
        "password": "adminpassword"
    })
    assert login_response.status_code == 200, f"Admin login failed: {login_response.content}"
    
    return login_response.json()["access_token"]

def test_get_user_profile(client, user_token, db):
    user_id = 1  # Assuming this is the ID of the registered user
    response = client.get(f"/api/v1/users/profile/{user_id}", headers={"Authorization": f"Bearer {user_token}"})
    print(f"Get user profile response: {response.status_code}")
    print(f"Response content: {response.content}")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_get_user_profile_not_found(client, user_token, db):
    user_id = 999  # Non-existent user ID
    response = client.get(f"/api/v1/users/profile/{user_id}", headers={"Authorization": f"Bearer {user_token}"})
    print(f"Get non-existent user profile response: {response.status_code}")
    print(f"Response content: {response.content}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_get_user_profile_unauthorized(client, user_token, db):
    # First, create another user
    register_response = client.post("/api/v1/auth/register", json={
        "username": "anotheruser",
        "email": "another@example.com",
        "password": "anotherpassword",
        "role": "user"
    })
    assert register_response.status_code == 201, f"Another user registration failed: {register_response.content}"
    
    # Assume the new user has ID 2 (as it's the second user created)
    another_user_id = 2
    
    # Try to access the other user's profile with the original user's token
    response = client.get(f"/api/v1/users/profile/{another_user_id}", headers={"Authorization": f"Bearer {user_token}"})
    print(f"Get unauthorized user profile response: {response.status_code}")
    print(f"Response content: {response.content}")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized to view this profile"}

def test_update_user_profile(client, user_token, db):
    user_id = 1  # Assuming this is the ID of the registered user
    update_data = {
        "full_name": "Updated Name",
        "bio": "Updated bio",
        "location": "Updated City"
    }
    response = client.put(f"/api/v1/users/profile/{user_id}", json=update_data, headers={"Authorization": f"Bearer {user_token}"})
    print(f"Update user profile response: {response.status_code}")
    print(f"Response content: {response.content}")
    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Name"
    assert response.json()["bio"] == "Updated bio"
    assert response.json()["location"] == "Updated City"

def test_update_user_profile_not_found(client, user_token, db):
    user_id = 999  # Non-existent user ID
    update_data = {"full_name": "Updated Name"}
    response = client.put(f"/api/v1/users/profile/{user_id}", json=update_data, headers={"Authorization": f"Bearer {user_token}"})
    print(f"Update non-existent user profile response: {response.status_code}")
    print(f"Response content: {response.content}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_update_user_profile_unauthorized(client, db):
    # Create first user
    register_response1 = client.post("/api/v1/auth/register", json={
        "username": "user1",
        "email": "user1@example.com",
        "password": "password1",
        "role": "user"
    })
    assert register_response1.status_code == 201, f"First user registration failed: {register_response1.content}"
    
    # Log in as first user to get token
    login_response1 = client.post("/api/v1/auth/login", json={
        "username": "user1",
        "password": "password1"
    })
    assert login_response1.status_code == 200, f"First user login failed: {login_response1.content}"
    user1_token = login_response1.json()["access_token"]

    # Create second user
    register_response2 = client.post("/api/v1/auth/register", json={
        "username": "user2",
        "email": "user2@example.com",
        "password": "password2",
        "role": "user"
    })
    assert register_response2.status_code == 201, f"Second user registration failed: {register_response2.content}"
    
    # Assume the second user has ID 2
    user2_id = 2

    # Try to update the second user's profile with the first user's token
    update_data = {"full_name": "Unauthorized Update"}
    response = client.put(f"/api/v1/users/profile/{user2_id}", json=update_data, headers={"Authorization": f"Bearer {user1_token}"})
    print(f"Update unauthorized user profile response: {response.status_code}")
    print(f"Response content: {response.content}")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized to update this profile"}

def test_admin_can_view_any_profile(client, admin_token, db):
    # First, create a regular user
    register_response = client.post("/api/v1/auth/register", json={
        "username": "regularuser",
        "email": "regularuser@example.com",
        "password": "userpassword",
        "role": "user",
        "full_name": "Regular User",
        "bio": "Regular user bio",
        "location": "User City"
    })
    assert register_response.status_code == 201, f"Regular user registration failed: {register_response.content}"
    
    # Get the user ID by querying all users (admin privilege)
    users_response = client.get("/api/v1/users/admin/users", headers={"Authorization": f"Bearer {admin_token}"})
    assert users_response.status_code == 200, f"Failed to get users: {users_response.content}"
    user_id = next(user['id'] for user in users_response.json() if user['username'] == 'regularuser')

    response = client.get(f"/api/v1/users/profile/{user_id}", headers={"Authorization": f"Bearer {admin_token}"})
    print(f"Admin view user profile response: {response.status_code}")
    print(f"Response content: {response.content}")
    assert response.status_code == 200
    assert response.json()["username"] == "regularuser"

def test_admin_can_update_any_profile(client, admin_token, db):
    # First, create a regular user
    register_response = client.post("/api/v1/auth/register", json={
        "username": "anotheruser",
        "email": "anotheruser@example.com",
        "password": "userpassword",
        "role": "user",
        "full_name": "Another User",
        "bio": "Another user bio",
        "location": "Another City"
    })
    assert register_response.status_code == 201, f"Another user registration failed: {register_response.content}"
    
    # Get the user ID by querying all users (admin privilege)
    users_response = client.get("/api/v1/users/admin/users", headers={"Authorization": f"Bearer {admin_token}"})
    assert users_response.status_code == 200, f"Failed to get users: {users_response.content}"
    user_id = next(user['id'] for user in users_response.json() if user['username'] == 'anotheruser')

    update_data = {"full_name": "Admin Updated Name"}
    response = client.put(f"/api/v1/users/profile/{user_id}", json=update_data, headers={"Authorization": f"Bearer {admin_token}"})
    print(f"Admin update user profile response: {response.status_code}")
    print(f"Response content: {response.content}")
    assert response.status_code == 200
    assert response.json()["full_name"] == "Admin Updated Name"
