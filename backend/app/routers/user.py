"""
API routes for User-related operations.
- Provides endpoints for user creation and retrieval by ID
- Leverages UserService for handling business logic
- Implements validation for unique email registration and error handling for missing users
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, User

router = APIRouter()

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user in the system.
    - Validates if the email is already registered.
    - If the email is taken, raises an HTTP 400 error.
    - Otherwise, creates and returns the new user.
    """
    db_user = UserService.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return UserService.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve user details by user ID.
    - If the user is not found, raises an HTTP 404 error.
    - Returns the user data if found.
    """
    db_user = UserService.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
