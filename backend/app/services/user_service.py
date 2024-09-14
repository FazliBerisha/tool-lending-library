# app/services/user_service.py
"""
Service layer for User-related operations.
- Implements business logic for user management
- Methods for creating users, getting users by email, etc.
"""

from sqlalchemy.orm import Session
from app.models.user import User
from app.core.auth import hash_password

class UserService:
    @staticmethod
    def create_user(db: Session, username: str, email: str, password: str):
        hashed_password = hash_password(password)
        user = User(username=username, email=email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()