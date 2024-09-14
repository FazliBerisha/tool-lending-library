# app/schemas/tool.py
"""
Defines Pydantic models for tool-related operations.
- ToolBase: Base model with common attributes
- ToolCreate: Schema for creating a new tool
- Tool: Schema for tool responses, including database id
"""

from pydantic import BaseModel

class ToolBase(BaseModel):
    name: str
    description: str
    category: str

class ToolCreate(ToolBase):
    pass

class Tool(ToolBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True