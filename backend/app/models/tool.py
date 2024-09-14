# app/models/tool.py
"""
Defines the Tool model for the database.
- Represents the 'tools' table in the database
- Includes fields for tool information (id, name, description, category)
- Establishes a relationship with the User model (owner)
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    category = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tools")