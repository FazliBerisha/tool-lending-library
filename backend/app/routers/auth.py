"""
Authentication routes for user registration and login.

This module provides the API endpoints for user authentication:
- Allows new users to register an account.
- Handles user login and generates JWT tokens for authenticated sessions.
- Leverages the user service for database operations such as user creation and lookup.
- Implements basic error handling for invalid login attempts, ensuring security.

Routes:
- `POST /register`: Registers a new user by accepting a username, email, and password, and stores the user's details in the database.
- `POST /login`: Authenticates a user by verifying the provided credentials and returns a JWT access token upon successful login.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import create_user, get_user_by_username
from app.core.auth import verify_password, create_access_token

auth_router = APIRouter()

valid_roles = ["user", "admin"]

@auth_router.post("/register")
def register_user(username: str, email: str, password: str, role: str = "user", db: Session = Depends(get_db)):
    """
    Registers a new user in the system with an optional role (default is 'user').

    Args:
    - username (str): The desired username for the new user.
    - email (str): The email address for the new user.
    - password (str): The plaintext password, which will be hashed before storing.
    - role (str, optional): The role of the user, default is 'user'. Must be one of the valid roles ('user', 'admin').
    - db (Session): A database session object for interacting with the database.

    Raises:
    - HTTPException: If the provided role is invalid (i.e., not in the allowed roles).

    Returns:
    - dict: A success message indicating successful user registration.
    """
    if role not in valid_roles:
        raise HTTPException(status_code=400, detail="Invalid role")

    # Creates a new user with the specified role
    user = create_user(db, username, email, password, role)
    return {"msg": "User registered successfully"}


@auth_router.post("/login")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    """
    Authenticates a user and returns a JWT token.

    Args:
    - username (str): The user's username.
    - password (str): The user's plain text password.
    - db (Session): Database session dependency to retrieve user data.

    Returns:
    - A JSON response with the access token and token type.
    - Raises an HTTPException if the credentials are invalid.
    """
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Modified token creation to include 'role' in the token payload for RBAC purposes
    access_token = create_access_token(data={"sub": user.username}, role=user.role)
    return {"access_token": access_token, "token_type": "bearer"}