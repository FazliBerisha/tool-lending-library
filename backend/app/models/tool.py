"""
Represents the Tool model in the database.

This model defines the structure of the 'tools' table, which stores information about various tools available in the system. It also establishes a relationship with the User model, linking each tool to its owner.

Attributes:
- `id` (Integer): Primary key and unique identifier for each tool.
- `name` (String): Name of the tool, indexed for optimized querying.
- `description` (String): Brief description of the tool.
- `category` (String): Tool category, indexed for efficient search operations.
- `owner_id` (Integer): Foreign key linking the tool to its owner's `id` in the User model.

Relationships:
- `owner`: Establishes a many-to-one relationship with the User model, linking tools to their respective owners.
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