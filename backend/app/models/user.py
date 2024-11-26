"""
This module defines the `User` model for interacting with the 'users' table in the database.

Key Components:
- The `User` class inherits from `Base` (SQLAlchemy base class).
- The table is named 'users', with columns for user data:
  - `id`: Primary key, uniquely identifies each user.
  - `username`: Unique and indexed string field for the user's username (nullable).
  - `email`: Unique and indexed string field for the user's email.
  - `hashed_password`: String field for storing the hashed password of the user.
  - `is_active`: Boolean field indicating if the user is active, with a default value of True.
  - `role`: Enum field defining the user's role, with options specified in `VALID_ROLES`.

Relationships:
- `tools`: Defines a one-to-many relationship with the `Tool` model, linking tools to their respective owners.
"""

from sqlalchemy import Boolean, Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from app.config import VALID_ROLES

class User(Base):
    """
    Represents the User model, mapping to the 'users' table in the database.
    Each user has attributes like id, username, email, hashed password, active status, and role.
    """
    __tablename__ = "users"  # Name of the table in the database

    # Unique identifier for each user (primary key), auto-incremented
    id = Column(Integer, primary_key=True, index=True)
    
    # The user's username, must be unique and indexed for quick lookup
    username = Column(String, unique=True, index=True)
    
    # The user's email, also unique and indexed
    email = Column(String, unique=True, index=True)
    
    # Stores the hashed version of the user's password
    hashed_password = Column(String)
    
    # Indicates if the user's account is active, defaults to True
    is_active = Column(Boolean, default=True)
    
    # The role of the user, chosen from predefined valid roles (e.g., 'admin', 'user')
    role = Column(Enum(*VALID_ROLES, name="user_roles"), default="user")

    # One-to-many relationship: A user can own multiple tools, linked through the `Tool` model
    tools = relationship("Tool", back_populates="owner")

    # User profile fields
    full_name = Column(String, nullable=True)

    bio = Column(String, nullable=True)

    location = Column(String, nullable=True)

    profile_picture = Column(String, nullable=True)  # URL to profile picture

    # Add the relationship to Reservation
    reservations = relationship("Reservation", back_populates="user")

    # Add this to your existing User class
    tool_submissions = relationship("ToolSubmission", back_populates="user")
