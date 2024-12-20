from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ToolBase(BaseModel):
    """
    Base class for common tool attributes.
    
    Attributes:
    - `name` (str): The name of the tool.
    - `description` (str): A brief description of the tool.
    - `category` (str): The category or type of the tool.
    - `condition` (str): The condition of the tool.
    - `image_url` (Optional[str]): The URL of the tool's image.
    """
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    condition: Optional[str] = None
    image_url: Optional[str] = None

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
    - `is_available` (bool): Indicates if the tool is available for use.
    - `created_at` (datetime): The date and time when the tool was created.
    
    Configuration:
    - `orm_mode` (bool): Allows the model to be used with SQLAlchemy ORM objects.
    """
    id: int
    owner_id: int
    is_available: bool
    created_at: datetime

    class Config:
        orm_mode = True  # Enables SQLAlchemy ORM compatibility

class ToolUpdate(BaseModel):
    """
    Model for updating tool details. All fields are optional to allow for partial updates.
    
    Attributes:
    - `name` (Optional[str]): An optional new name for the tool.
    - `description` (Optional[str]): An optional new description for the tool.
    - `category` (Optional[str]): An optional new category for the tool.
    - `condition` (Optional[str]): An optional new condition for the tool.
    - `image_url` (Optional[str]): An optional new image URL for the tool.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    condition: Optional[str] = None
    image_url: Optional[str] = None
