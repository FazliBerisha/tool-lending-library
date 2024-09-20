"""
Service layer for handling user-related operations.

This module provides methods for user management, including creation, retrieval, and role updates. 
It serves as the business logic layer, interacting with the database and applying any necessary rules 
for user operations. This service ensures that operations such as user creation, retrieval by ID or email, 
and role updates are handled consistently.

Functions:
- `create_user`: Creates a new user with optional role validation.
- `get_user`: Retrieves a user by their ID.
- `get_user_by_email`: Retrieves a user by their email address.
- `get_user_by_username`: Retrieves a user by their username.
- `update_user_role`: Updates the role of an existing user.
- `get_all_users`: Retrieves all users from the database.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import get_password_hash
from app.config import VALID_ROLES
from app.schemas.user import UserCreate

class UserService:
    @staticmethod
    def create_user(db: Session, username: str, email: str, password: str, role: str = "user") -> User:
        """
        Creates a new user in the database.

        Parameters:
        - `db` (Session): The database session used for creating the user.
        - `username` (str): The username for the new user.
        - `email` (str): The email address for the new user.
        - `password` (str): The password for the new user.
        - `role` (str, optional): The role for the new user. Defaults to "user".

        Returns:
        - User: The newly created user record.

        Raises:
        - HTTPException: If the provided role is not valid.
        """
        if role not in VALID_ROLES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")

        hashed_password = get_password_hash(password)
        db_user = User(username=username, email=email, hashed_password=hashed_password, role=role)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        """
        Retrieves a user by their ID.

        Parameters:
        - `db` (Session): The database session used for querying.
        - `user_id` (int): The ID of the user to retrieve.

        Returns:
        - User: The user record corresponding to the provided ID.

        Raises:
        - HTTPException: If the user is not found.
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """
        Retrieves a user by their email address.

        Parameters:
        - `db` (Session): The database session used for querying.
        - `email` (str): The email address of the user to retrieve.

        Returns:
        - User: The user record corresponding to the provided email address.
        """
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """
        Retrieves a user by their username.

        Parameters:
        - `db` (Session): The database session used for querying.
        - `username` (str): The username of the user to retrieve.

        Returns:
        - User: The user record corresponding to the provided username.

        Raises:
        - HTTPException: If the user is not found.
        """
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    def update_user_role(db: Session, user_id: int, new_role: str) -> User:
        """
        Updates the role of an existing user.

        Parameters:
        - `db` (Session): The database session used for updating the user.
        - `user_id` (int): The ID of the user whose role is to be updated.
        - `new_role` (str): The new role to assign to the user.

        Returns:
        - User: The updated user record.

        Raises:
        - HTTPException: If the provided role is not valid or the user is not found.
        """
        if new_role not in VALID_ROLES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user.role = new_role
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_all_users(db: Session):
        """
        Retrieves all users from the database.

        Parameters:
        - `db` (Session): The database session used for querying.

        Returns:
        - List[User]: A list of all user records in the database.
        """
        return db.query(User).all()
