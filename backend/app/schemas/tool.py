"""
Defines Pydantic models for tool-related operations.

These models are responsible for validating input data and formatting output data related to tools in the system. Each model is tailored for specific operations like creating, reading, and updating tools.

Classes:
- `ToolBase`: A base model that includes the common fields for all tool-related operations.
- `ToolCreate`: A model that inherits from `ToolBase`, designed for creating new tools.
- `Tool`: A model that extends `ToolBase`, used for reading tool details from the database and includes additional fields like `id` and `owner_id`.
- `ToolUpdate`: A model designed for updating tool details, with all fields being optional to allow partial updates.
"""

from pydantic import BaseModel
from typing import Optional

class ToolBase(BaseModel):
    """
    Base class for common tool attributes.
    
    Attributes:
    - `name` (str): The name of the tool.
    - `description` (str): A brief description of the tool.
    - `category` (str): The category or type of the tool.
    """
    name: str
    description: str
    category: str

class ToolCreate(ToolBase):
    """
    Inherits from `ToolBase`. Used for validating input when creating new tools.
    
    All fields from `ToolBase` are required when creating a new tool.
    """
    pass

class Tool(ToolBase):
    """
    Extends `ToolBase` to include additional fields that are returned when querying tool details from the database.
    
    Attributes:
    - `id` (int): The unique identifier of the tool.
    - `owner_id` (int): The ID of the user who owns the tool.
    
    Configuration:
    - `orm_mode` (bool): Allows the model to be used with SQLAlchemy ORM objects.
    """
    id: int
    owner_id: int

    class Config:
        orm_mode = True  # Enables SQLAlchemy ORM compatibility

class ToolUpdate(BaseModel):
    """
    Model for updating tool details. All fields are optional to allow for partial updates.
    
    Attributes:
    - `name` (Optional[str]): An optional new name for the tool.
    - `description` (Optional[str]): An optional new description for the tool.
    - `category` (Optional[str]): An optional new category for the tool.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
