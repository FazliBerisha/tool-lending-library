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

@router.post("/sample", status_code=201)
def create_sample_tools(db: Session = Depends(get_db)):
    """
    Create sample tool data in the database.
    - Used for seeding the database with initial or test data.
    """
    ToolService.create_sample_tools(db)
    return {"message": "Sample tools created successfully"}

@router.post("/", response_model=Tool)
def create_tool(tool: ToolCreate, db: Session = Depends(get_db)):
    """
    Create a new tool with the provided data.
    - `tool`: The details of the tool to be created.
    - Assigns ownership of the tool to a default owner (`owner_id=1`).
    """
    return ToolService.create_tool(db, tool, owner_id=1)
