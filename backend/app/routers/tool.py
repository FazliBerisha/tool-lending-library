from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.tool_service import ToolService
from app.schemas.tool import Tool, ToolCreate, ToolUpdate
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.reservation import Reservation, ReservationCreate
from app.services.reservation_service import ReservationService

router = APIRouter()

def get_current_user_id(current_user: User = Depends(get_current_user)) -> int:
    return current_user.id

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

@router.post("/sample", status_code=status.HTTP_201_CREATED)
def create_sample_tools(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create sample tools")
    created_tools = ToolService.create_sample_tools(db)
    return {"message": "Sample tools created successfully", "tools": created_tools}

@router.post("/", response_model=Tool, status_code=status.HTTP_201_CREATED)
def create_tool(
    tool: ToolCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create tools")
    return ToolService.create_tool(db, tool, owner_id=current_user.id)

@router.put("/{tool_id}", response_model=Tool)
def update_tool(
    tool_id: int,
    tool: ToolUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update tools")
    updated_tool = ToolService.update_tool(db, tool_id, tool)
    if updated_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return updated_tool

@router.delete("/{tool_id}", status_code=204)
def delete_tool(
    tool_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete tools")
    if not ToolService.delete_tool(db, tool_id):
        raise HTTPException(status_code=404, detail="Tool not found")
    return Response(status_code=204)

