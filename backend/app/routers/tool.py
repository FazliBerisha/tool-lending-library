# app/routers/tool.py
"""
Defines API routes for tool-related operations.
- Includes endpoints for listing, searching, and filtering tools
- Handles creation of new tools and sample data
- Uses ToolService for database operations
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
    tools = ToolService.get_tools(db, skip=skip, limit=limit)
    return tools

@router.get("/search/", response_model=List[Tool])
def search_tools(search_term: str, db: Session = Depends(get_db)):
    tools = ToolService.search_tools(db, search_term)
    return tools

@router.get("/category/{category}", response_model=List[Tool])
def get_tools_by_category(category: str, db: Session = Depends(get_db)):
    tools = ToolService.get_tools_by_category(db, category)
    return tools

@router.post("/sample", status_code=201)
def create_sample_tools(db: Session = Depends(get_db)):
    ToolService.create_sample_tools(db)
    return {"message": "Sample tools created successfully"}

@router.post("/", response_model=Tool)
def create_tool(tool: ToolCreate, db: Session = Depends(get_db)):
    try:
        return ToolService.create_tool(db, tool, owner_id=1)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 