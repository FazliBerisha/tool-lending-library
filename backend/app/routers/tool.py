"""
Defines API routes for tool-related operations.
- Provides endpoints for listing, searching, and filtering tools
- Enables creation of new tools and sample tool data
- Leverages ToolService for database interactions
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.tool_service import ToolService
from app.schemas.tool import Tool, ToolCreate
from app.core.deps import role_required

router = APIRouter()

@router.get("/", response_model=List[Tool])
def read_tools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Fetch a list of tools with pagination support.
    - `skip`: Number of records to skip
    - `limit`: Maximum number of records to return
    """
    tools = ToolService.get_tools(db, skip=skip, limit=limit)
    return tools

@router.get("/search/", response_model=List[Tool])
def search_tools(search_term: str, db: Session = Depends(get_db)):
    """
    Search tools by a specific term in their name or description.
    - `search_term`: The term to search for within tools.
    """
    tools = ToolService.search_tools(db, search_term)
    return tools

@router.get("/category/{category}", response_model=List[Tool])
def get_tools_by_category(category: str, db: Session = Depends(get_db)):
    """
    Retrieve tools by category.
    - `category`: The category to filter tools by.
    """
    tools = ToolService.get_tools_by_category(db, category)
    return tools

# Added the role-based access control (RBAC) check using role_required to restrict this endpoint to 'admin' role
@router.post("/sample", status_code=201, dependencies=[Depends(role_required("admin"))])
def create_sample_tools(db: Session = Depends(get_db)):
    """
    Endpoint for creating sample tool data, restricted to 'admin' users.
    - The 'role_required' dependency ensures that only 'admin' users can access this route.
    
    Args:
    - db (Session): The database session to use for database operations.
    
    Returns:
    - A success message when the sample tools are created.
    """
    ToolService.create_sample_tools(db)
    return {"message": "Sample tools created successfully"}

# Added the role-based access control (RBAC) check using role_required to restrict this endpoint to 'admin' role
@router.post("/", response_model=Tool, dependencies=[Depends(role_required("admin"))])
def create_tool(tool: ToolCreate, db: Session = Depends(get_db)):
    """
    Create a new tool with the provided data.
    - `tool`: The details of the tool to be created.
    - Assigns ownership of the tool to a default owner (`owner_id=1`).
    """
    return ToolService.create_tool(db, tool, owner_id=1)

