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
- `reservations`: Establishes a many-to-one relationship with the Reservation model, linking tools to their respective reservations.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Tool(Base):
    """
    The Tool model represents a tool entity in the 'tools' table.
    Each tool is linked to a user (the owner) via a foreign key.
    """
    __tablename__ = "tools"  # Name of the table in the database

    # Primary key for each tool, unique and auto-incremented
    id = Column(Integer, primary_key=True, index=True)
    
    # Name of the tool, indexed for faster search performance
    name = Column(String, index=True)
    
    # Brief description of the tool, explaining its purpose or features
    description = Column(String)
    
    # Category to which the tool belongs (e.g., "Software", "Hardware"), also indexed
    category = Column(String, index=True)
    
    # Foreign key connecting each tool to its owner's user ID
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Many-to-one relationship with the User model, indicating that each tool is owned by a single user
    owner = relationship("User", back_populates="tools")

    # Many-to-one relationship with the Reservation model, indicating that each tool can have multiple reservations
    reservations = relationship("Reservation", back_populates="tool")
