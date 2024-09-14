# app/models/user.py
"""
Defines the User model for the database.
- Represents the 'users' table in the database
- Includes fields for user information (id, username, email, password)
- Establishes a relationship with the Tool model
"""

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    tools = relationship("Tool", back_populates="owner")
