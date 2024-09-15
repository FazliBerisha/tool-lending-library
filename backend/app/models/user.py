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

Relationships:
- `tools`: Defines a one-to-many relationship with the `Tool` model, linking tools to their respective owners.
"""

from sqlalchemy import Boolean, Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  # Add role column with default as 'user'

    tools = relationship("Tool", back_populates="owner")