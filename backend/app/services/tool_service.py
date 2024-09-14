"""
Service layer for managing tool-related operations.
- Provides methods for CRUD operations on tools.
- Implements business logic, including search and filtering by category.
- Includes a method for creating a set of sample tools for demonstration purposes.
"""

from sqlalchemy.orm import Session
from app.models.tool import Tool
from app.schemas.tool import ToolCreate

class ToolService:
    @staticmethod
    def get_tools(db: Session, skip: int = 0, limit: int = 100):
        """
        Retrieve a list of tools from the database, with optional pagination.
        :param db: Database session object.
        :param skip: Number of records to skip (default: 0).
        :param limit: Maximum number of records to return (default: 100).
        :return: List of tools.
        """
        return db.query(Tool).offset(skip).limit(limit).all()

    @staticmethod
    def create_tool(db: Session, tool: ToolCreate, owner_id: int):
        """
        Create a new tool in the database.
        :param db: Database session object.
        :param tool: Pydantic model containing the tool data.
        :param owner_id: ID of the tool owner (user).
        :return: The newly created tool.
        """
        db_tool = Tool(**tool.dict(), owner_id=owner_id)
        db.add(db_tool)
        db.commit()
        db.refresh(db_tool)  # Refresh to retrieve the generated ID and any other defaults.
        return db_tool

    @staticmethod
    def search_tools(db: Session, search_term: str):
        """
        Search tools by their name, using case-insensitive matching.
        :param db: Database session object.
        :param search_term: Term to search for in tool names.
        :return: List of tools that match the search term.
        """
        return db.query(Tool).filter(Tool.name.ilike(f"%{search_term}%")).all()

    @staticmethod
    def get_tools_by_category(db: Session, category: str):
        """
        Retrieve tools by their category.
        :param db: Database session object.
        :param category: The category of tools to filter by.
        :return: List of tools in the specified category.
        """
        return db.query(Tool).filter(Tool.category == category).all()

    @staticmethod
    def create_sample_tools(db: Session):
        """
        Create a set of sample tools for testing or demonstration purposes.
        :param db: Database session object.
        :return: None.
        """
        sample_tools = [
            {"name": "Power Drill", "description": "Cordless power drill", "category": "Power Tools"},
            {"name": "Hammer", "description": "Claw hammer", "category": "Hand Tools"},
            {"name": "Circular Saw", "description": "Electric circular saw", "category": "Power Tools"},
            {"name": "Screwdriver Set", "description": "Set of Phillips and flathead screwdrivers", "category": "Hand Tools"},
            {"name": "Wrench Set", "description": "Set of adjustable wrenches", "category": "Hand Tools"}
        ]
        
        for tool in sample_tools:
            db_tool = Tool(**tool, owner_id=1)  # Assume owner_id 1 for the sample tools
            db.add(db_tool)
        
        db.commit()  # Commit once after adding all tools
