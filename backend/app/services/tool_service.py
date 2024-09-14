# app/services/tool_service.py
"""
Service layer for tool-related operations.
- Provides methods for CRUD operations on tools
- Implements business logic for tool management
- Includes method for creating sample tools
"""

from sqlalchemy.orm import Session
from app.models.tool import Tool
from app.schemas.tool import ToolCreate

class ToolService:
    @staticmethod
    def get_tools(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Tool).offset(skip).limit(limit).all()

    @staticmethod
    def create_tool(db: Session, tool: ToolCreate, owner_id: int):
        db_tool = Tool(**tool.dict(), owner_id=owner_id)
        db.add(db_tool)
        db.commit()
        db.refresh(db_tool)
        return db_tool

    @staticmethod
    def search_tools(db: Session, search_term: str):
        return db.query(Tool).filter(Tool.name.ilike(f"%{search_term}%")).all()

    @staticmethod
    def get_tools_by_category(db: Session, category: str):
        return db.query(Tool).filter(Tool.category == category).all()

    @staticmethod
    def create_sample_tools(db: Session):
        sample_tools = [
            {"name": "Power Drill", "description": "Cordless power drill", "category": "Power Tools"},
            {"name": "Hammer", "description": "Claw hammer", "category": "Hand Tools"},
            {"name": "Circular Saw", "description": "Electric circular saw", "category": "Power Tools"},
            {"name": "Screwdriver Set", "description": "Set of Phillips and flathead screwdrivers", "category": "Hand Tools"},
            {"name": "Wrench Set", "description": "Set of adjustable wrenches", "category": "Hand Tools"}
        ]
        for tool in sample_tools:
            db_tool = Tool(**tool, owner_id=1) 
            db.add(db_tool)
        db.commit()