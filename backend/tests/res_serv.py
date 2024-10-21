import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app  # Assuming your FastAPI app is called `app` in `main.py`
from app.database import Base, get_db
from app.models.tool import Tool
from app.models.user import User

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the testing database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the database schema
Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture
def create_test_data():
    """Fixture to create initial test data (tools and users) in the database."""
    db = TestingSessionLocal()
    user = User(username="testuser", email="test@example.com", hashed_password="fakehashedpassword")
    tool = Tool(name="Hammer", description="A useful hammer", category="Hand Tools", available=True)
    db.add(user)
    db.add(tool)
    db.commit()
    db.refresh(user)
    db.refresh(tool)
    yield {"user": user, "tool": tool}
    db.close()

def test_check_out_tool(create_test_data):
    """Test that a tool can be checked out successfully."""
    tool = create_test_data["tool"]
    user = create_test_data["user"]
    
    # Simulate a login (you might need to adjust this part if you have authentication)
    response = client.post(f"/tools/{tool.id}/checkout", headers={"Authorization": f"Bearer {user.id}"})
    
    assert response.status_code == 200
    response_data = response.json()
    
    assert response_data["id"] == tool.id
    assert not response_data["available"]  # Tool should be marked unavailable
    assert response_data["checked_out_by"] == user.id  # Tool should be checked out by the user

def test_return_tool(create_test_data):
    """Test that a tool can be returned successfully."""
    tool = create_test_data["tool"]
    user = create_test_data["user"]
    
    # First, check out the tool
    client.post(f"/tools/{tool.id}/checkout", headers={"Authorization": f"Bearer {user.id}"})
    
    # Now return the tool
    response = client.post(f"/tools/{tool.id}/return", headers={"Authorization": f"Bearer {user.id}"})
    
    assert response.status_code == 200
    response_data = response.json()
    
    assert response_data["id"] == tool.id
    assert response_data["available"]  # Tool should be marked available
    assert response_data["checked_out_by"] is None  # No user should be associated with the tool
