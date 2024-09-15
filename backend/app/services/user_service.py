"""
Service layer for handling user-related operations.
- Manages business logic for user creation, retrieval, and management.
- Provides methods to create users, find users by email, and retrieve user details by ID.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

valid_roles = ["user", "admin"]

class UserService:
    @staticmethod
    def create_user(db: Session, user: UserCreate, role: str = "user") -> User:
        """
        Create a new user in the database, with an optional role (default 'user').
        - Hashes the user's password before storing it.
        - Adds the new user to the database and commits the transaction.
        
        Args:
        - db (Session): Database session object.
        - user (UserCreate): Pydantic model containing user creation data.
        - role (str): The role of the user. Must be one of the valid roles. Defaults to 'user'.
        
        Returns:
        - User: The newly created user.
        
        Raises:
        - HTTPException: If the provided role is invalid.
        """
        if role not in valid_roles:
            raise HTTPException(status_code=400, detail="Invalid role")

        hashed_password = get_password_hash(user.password)
        db_user = User(username=user.username, email=user.email, hashed_password=hashed_password, role=role)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)  # Refresh to get the ID and other default values
        return db_user

    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        """
        Retrieve a user by their ID.
        
        Args:
        - db (Session): Database session object.
        - user_id (int): ID of the user to retrieve.
        
        Returns:
        - User: User object if found, else None.
        
        Raises:
        - HTTPException: If the user is not found.
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """
        Retrieve a user by their email address.
        
        Args:
        - db (Session): Database session object.
        - email (str): Email address of the user to retrieve.
        
        Returns:
        - User: User object if found, else None.
        
        Raises:
        - HTTPException: If the user is not found.
        """
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    def update_user_role(db: Session, user_id: int, new_role: str) -> User:
        """
        Update the role of a user.
        
        Args:
        - db (Session): Database session object.
        - user_id (int): ID of the user whose role needs to be updated.
        - new_role (str): The new role for the user. Must be one of the valid roles.
        
        Returns:
        - User: The updated user object.
        
        Raises:
        - HTTPException: If the role is invalid or the user is not found.
        """
        if new_role not in valid_roles:
            raise HTTPException(status_code=400, detail="Invalid role")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.role = new_role
        db.commit()
        db.refresh(user)
        return user
