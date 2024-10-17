import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.config import settings
from app.models import user, tool  # Import all your models

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create an SQLAlchemy engine for the testing database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured session factory for the testing database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """
    Override the `get_db` dependency to use the testing database session.
    
    This function provides a database session that uses the in-memory SQLite database 
    configured for testing. It ensures that the session is closed after use.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def db():
    """
    Fixture for providing a new database session for each test function.
    
    This fixture sets up the database schema before each test function and tears it down 
    after the test function completes. It ensures a clean state for each test function.
    """
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    """
    Fixture for providing a FastAPI test client.
    
    This fixture sets up the FastAPI application with the overridden database dependency for
    testing. It provides a test client that can be used to make requests to the application.
    It creates the database schema before the tests and drops it after the tests are complete.
    """
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

# Override settings for testing
settings.DATABASE_URL = SQLALCHEMY_DATABASE_URL

@pytest.fixture(scope="function")
def user_token(client, db):
    register_response = client.post("/api/v1/auth/register", json={
        "username": "user",
        "email": "user@example.com",
        "password": "userpassword",
        "role": "user",
        "full_name": "Test User",
        "bio": "Test bio",
        "location": "Test City"
    })

@pytest.fixture(scope="function")
def admin_token(client, db):
    register_response = client.post("/api/v1/auth/register", json={
        "username": "admin",
        "email": "admin@example.com",
        "password": "adminpassword",
        "role": "admin",
        "full_name": "Admin User",
        "bio": "Admin bio",
        "location": "Admin City"
    })
