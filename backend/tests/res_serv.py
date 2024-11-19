from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app  # Ensure app is correctly imported
from app.services.review_service import ReportService
from app.core.auth import get_current_user_role

client = TestClient(app)

# Mock data simulating the most borrowed tools response
mock_borrowed_tools_data = [
    {"tool_name": "Drill", "borrow_count": 15},
    {"tool_name": "Hammer", "borrow_count": 10},
    {"tool_name": "Saw", "borrow_count": 8}
]

# Mock user role functions
def mock_get_current_user_role_admin():
    return "admin"

def mock_get_current_user_role_non_admin():
    return "user"

# Test for unauthorized (non-admin) access
def test_most_borrowed_tools_unauthorized():
    app.dependency_overrides[get_current_user_role] = mock_get_current_user_role_non_admin
    response = client.get("/api/v1/reports/most-borrowed-tools?limit=5")
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 403  # Expect 403 Forbidden for non-admin
    app.dependency_overrides = {}  # Reset overrides after test

# Test for authorized admin access with a mocked response
@patch("app.services.review_service.ReportService.get_most_borrowed_tools")
def test_most_borrowed_tools_as_admin(mock_get_most_borrowed_tools):
    app.dependency_overrides[get_current_user_role] = mock_get_current_user_role_admin
    mock_get_most_borrowed_tools.return_value = mock_borrowed_tools_data
    response = client.get("/api/v1/reports/most-borrowed-tools?limit=5")
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 200
    assert response.json() == mock_borrowed_tools_data  # Should match mock data
    app.dependency_overrides = {}  # Reset overrides after test

# Test with varying limits to ensure correct data slicing
@patch("app.services.review_service.ReportService.get_most_borrowed_tools")
def test_most_borrowed_tools_with_different_limits(mock_get_most_borrowed_tools):
    app.dependency_overrides[get_current_user_role] = mock_get_current_user_role_admin
    for limit in [1, 2, 3]:
        mock_get_most_borrowed_tools.return_value = mock_borrowed_tools_data[:limit]
        response = client.get(f"/api/v1/reports/most-borrowed-tools?limit={limit}")
        print("Response status code:", response.status_code)
        print("Response JSON:", response.json())
        assert response.status_code == 200
        assert response.json() == mock_borrowed_tools_data[:limit]
    app.dependency_overrides = {}  # Reset overrides after loop

# Mock data for least borrowed tools
mock_least_borrowed_tools_data = [
    {"tool_name": "Screwdriver", "borrow_count": 2},
    {"tool_name": "Wrench", "borrow_count": 3},
    {"tool_name": "Pliers", "borrow_count": 5},
]

def test_least_borrowed_tools_unauthorized():
    app.dependency_overrides[get_current_user_role] = mock_get_current_user_role_non_admin
    response = client.get("/api/v1/reports/least-borrowed-tools?limit=5")
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 403  # Expecting Forbidden for non-admin
    app.dependency_overrides = {}  # Reset overrides after test

@patch("app.services.review_service.ReportService.get_least_borrowed_tools")
def test_least_borrowed_tools_as_admin(mock_get_least_borrowed_tools):
    app.dependency_overrides[get_current_user_role] = mock_get_current_user_role_admin
    mock_get_least_borrowed_tools.return_value = mock_least_borrowed_tools_data
    response = client.get("/api/v1/reports/least-borrowed-tools?limit=5")
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 200
    assert response.json() == mock_least_borrowed_tools_data
    app.dependency_overrides = {}  # Reset overrides after test

@patch("app.services.review_service.ReportService.get_least_borrowed_tools")
def test_least_borrowed_tools_with_different_limits(mock_get_least_borrowed_tools):
    app.dependency_overrides[get_current_user_role] = mock_get_current_user_role_admin
    for limit in [1, 2, 3]:
        mock_get_least_borrowed_tools.return_value = mock_least_borrowed_tools_data[:limit]
        response = client.get(f"/api/v1/reports/least-borrowed-tools?limit={limit}")
        print("Response status code:", response.status_code)
        print("Response JSON:", response.json())
        assert response.status_code == 200
        assert response.json() == mock_least_borrowed_tools_data[:limit]
    app.dependency_overrides = {}  # Reset overrides after loop
