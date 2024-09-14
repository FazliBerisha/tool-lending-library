"""
Service layer for handling user-related operations.
- Manages business logic for user creation, retrieval, and management.
- Provides methods to create users, find users by email, and retrieve user details by ID.
"""

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

class UserService:
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        """
        Create a new user in the database.
        - Hashes the user's password before storing it.
        - Adds the new user to the database and commits the transaction.
        :param db: Database session object.
        :param user: Pydantic model containing user creation data.
        :return: The newly created user.
        """
        hashed_password = get_password_hash(user.password)
        db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)  # Refresh to get the ID and other default values
        return db_user

    @staticmethod
    def get_user(db: Session, user_id: int):
        """
        Retrieve a user by their ID.
        :param db: Database session object.
        :param user_id: ID of the user to retrieve.
        :return: User object if found, else None.
        """
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        """
        Retrieve a user by their email address.
        :param db: Database session object.
        :param email: Email address of the user to retrieve.
        :return: User object if found, else None.
        """
        return db.query(User).filter(User.email == email).first()
