"""
Authentication routes for user registration and login.

This module provides API endpoints for user authentication:
- Registers new users.
- Authenticates users and generates JWT tokens for session management.
- Utilizes the UserService for database operations such as user creation and lookup.
- Implements error handling for invalid login attempts to enhance security.

Routes:
- `POST /register`: Registers a new user with username, email, password, and optional role.
- `POST /login`: Authenticates a user, returning a JWT access token upon successful login.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import UserService
from app.core.security import verify_password
from app.core.auth import create_access_token
from app.config import settings
from pydantic import BaseModel

# Router for handling authentication-related routes
router = APIRouter()

# Pydantic model for user registration
class UserCreate(BaseModel):
    """
    Pydantic model for creating a new user.
    - `username`: The user's desired username.
    - `email`: The user's email address.
    - `password`: The user's password.
    - `role`: Optional role (default is 'user').
    """
    username: str
    email: str
    password: str
    role: str = "user"

# Pydantic model for user login
class UserLogin(BaseModel):
    """
    Pydantic model for user login.
    - `username`: The user's username.
    - `password`: The user's password.
    """
    username: str
    password: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user in the system with an optional role (default is 'user').
    
    Validates the provided role against the allowed roles defined in the settings.
    Creates the user in the database through the UserService.

    Args:
    - `user`: UserCreate model containing username, email, password, and role.
    - `db`: SQLAlchemy session for database access.

    Raises:
    - `HTTP_400_BAD_REQUEST`: If the role is invalid.
    
    Returns:
    - A success message upon successful registration.
    """
    # Check if the role is valid according to the configured roles
    if user.role not in settings.VALID_ROLES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")
    
    # Create and save the new user in the database
    new_user = UserService.create_user(db, user.username, user.email, user.password, user.role)
    
    return {"msg": "User registered successfully"}

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user and return a JWT token upon successful login.

    Args:
    - user: UserLogin model containing username and password.
    - db: SQLAlchemy session for database access.

    Returns:
    - A dictionary with the JWT access token, token type, user ID, and role.

    Raises:
    - HTTP_401_UNAUTHORIZED: If the credentials are incorrect.
    """
    db_user = UserService.get_user_by_username(db, user.username)
    
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": db_user.username}, role=db_user.role)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": db_user.id,
        "role": db_user.role
    }

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a user using form data and return a JWT token.

    Args:
    - `form_data`: OAuth2PasswordRequestForm containing the user's username and password.
    - `db`: SQLAlchemy session for database access.

    Raises:
    - `HTTP_401_UNAUTHORIZED`: If the credentials are incorrect.
    
    Returns:
    - A dictionary with the JWT access token and token type.
    """
    # Get user by username from the database
    user = UserService.get_user_by_username(db, form_data.username)
    
    # Verify the user's password
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate and return JWT access token
    access_token = create_access_token(data={"sub": user.username}, role=user.role)
    return {"access_token": access_token, "token_type": "bearer"}
