# app/models/user.py
"""
SQLAlchemy model for the User table.
- Defines User attributes (id, username, email, hashed_password)
- Sets up relationships with other models if any
"""

from sqlalchemy import Boolean, Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
