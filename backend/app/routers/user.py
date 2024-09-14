# app/routers/user.py
"""
API routes for User-related operations.
- Defines endpoints for user registration, retrieval, etc.
- Uses UserService for business logic
- Implements input validation and error handling
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, User

router = APIRouter()

@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserService.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return UserService.create_user(db=db, username=user.username, email=user.email, password=user.password)