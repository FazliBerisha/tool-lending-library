"""
Defines Pydantic models for tool-related operations.
- `ToolBase`: A base model that includes common tool attributes such as name, description, and category.
- `ToolCreate`: Inherits from `ToolBase`, used for creating new tools.
- `Tool`: Inherits from `ToolBase`, includes additional fields like id and owner_id for response models, and enables ORM mode.
"""

from pydantic import BaseModel

class ToolBase(BaseModel):
    """
    Base schema for tool data, used as a foundation for other models.
    """
    name: str
    description: str
    category: str

class ToolCreate(ToolBase):
    """
    Schema for creating a new tool, inherits all fields from ToolBase.
    """
    pass

class Tool(ToolBase):
    """
    Schema for tool response, includes database id and owner_id.
    - Enables ORM mode to allow compatibility with SQLAlchemy models.
    """
    id: int
    owner_id: int

    class Config:
        orm_mode = True
