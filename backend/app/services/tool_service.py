"""
Service layer for managing tool-related operations.

This module provides methods to handle CRUD (Create, Read, Update, Delete) operations for tools. 
It interacts with the database and applies any custom business rules when managing tools. 
The service includes functionality for searching tools by name or description and filtering by category.

Functions:
- `get_tools`: Retrieves tools with pagination.
- `create_tool`: Adds a new tool to the database.
- `search_tools`: Searches for tools by name or description.
- `get_tools_by_category`: Filters tools by category.
- `create_sample_tools`: Creates a set of predefined sample tools for testing.
- `update_tool`: Updates existing tool data.
- `delete_tool`: Deletes a tool from the database.
"""

from sqlalchemy.orm import Session
from app.models.tool import Tool  # Tool database model
from app.schemas.tool import ToolCreate, ToolUpdate  # Pydantic models for input validation

class ToolService:
    """
    This class contains static methods for core business logic related to tools.
    """

    @staticmethod
    def get_tools(db: Session, skip: int = 0, limit: int = 100):
        """
        Retrieves a list of tools from the database with pagination.

        Parameters:
        - `db` (Session): The database session for querying.
        - `skip` (int): Number of records to skip for pagination.
        - `limit` (int): Maximum number of records to return.

        Returns:
        - List of tools within the specified range.
        """
        return db.query(Tool).filter(Tool.is_available).offset(skip).limit(limit).all()

    @staticmethod
    def create_tool(db: Session, tool: ToolCreate, owner_id: int):
        """
        Creates and saves a new tool in the database.

        Parameters:
        - `db` (Session): The database session for interaction.
        - `tool` (ToolCreate): Data for the new tool.
        - `owner_id` (int): ID of the user who owns the tool.

        Returns:
        - The newly created tool record.
        """
        db_tool = Tool(**tool.dict(), owner_id=owner_id)  # Create tool instance
        db.add(db_tool)
        db.commit()  # Save to database
        db.refresh(db_tool)  # Refresh with latest data
        return db_tool

    @staticmethod
    def search_tools(db: Session, search_term: str):
        """
        Searches for tools by name or description using a search term.

        Parameters:
        - `db` (Session): The database session for querying.
        - `search_term` (str): Search string for matching tools.

        Returns:
        - List of tools matching the search term.
        """
        return db.query(Tool).filter(
            Tool.name.ilike(f"%{search_term}%") | Tool.description.ilike(f"%{search_term}%")
        ).all()

    @staticmethod
    def get_tools_by_category(db: Session, category: str):
        """
        Retrieves tools by a specific category.

        Parameters:
        - `db` (Session): The database session for querying.
        - `category` (str): The category to filter tools by.

        Returns:
        - List of tools in the specified category.
        """
        return db.query(Tool).filter(Tool.category == category).all()

    @staticmethod
    def create_sample_tools(db: Session):
        """
        Creates predefined sample tools for testing purposes.

        Parameters:
        - `db` (Session): The database session for saving sample tools.

        Returns:
        - List of created sample tools.
        """
        sample_tools = [
            {"name": "Power Drill", "description": "Cordless power drill", "category": "Power Tools"},
            {"name": "Hammer", "description": "Claw hammer", "category": "Hand Tools"},
            {"name": "Circular Saw", "description": "Electric circular saw", "category": "Power Tools"},
            {"name": "Screwdriver Set", "description": "Set of Phillips and flathead screwdrivers", "category": "Hand Tools"},
            {"name": "Wrench Set", "description": "Set of adjustable wrenches", "category": "Hand Tools"}
        ]

        created_tools = []
        for tool in sample_tools:
            db_tool = Tool(**tool, owner_id=1)  # Assume owner_id = 1 for sample data
            db.add(db_tool)
            created_tools.append(db_tool)

        db.commit()  # Save all sample tools to the database
        for tool in created_tools:
            db.refresh(tool)  # Refresh tool instances
        return created_tools

    @staticmethod
    def update_tool(db: Session, tool_id: int, tool_update: ToolUpdate):
        """
        Updates an existing tool's data.

        Parameters:
        - `db` (Session): The database session for updating.
        - `tool_id` (int): ID of the tool to update.
        - `tool_update` (ToolUpdate): Data for updating the tool.

        Returns:
        - The updated tool record, or None if the tool was not found.
        """
        db_tool = db.query(Tool).filter(Tool.id == tool_id).first()
        if db_tool is None:
            return None  # Tool not found
        for key, value in tool_update.dict(exclude_unset=True).items():
            setattr(db_tool, key, value)  # Update only provided fields
        db.commit()  # Save changes
        db.refresh(db_tool)  # Refresh updated tool
        return db_tool

    @staticmethod
    def delete_tool(db: Session, tool_id: int):
        """
        Deletes a tool from the database.

        Parameters:
        - `db` (Session): The database session for deletion.
        - `tool_id` (int): ID of the tool to delete.

        Returns:
        - True if the tool was deleted, otherwise False.
        """
        db_tool = db.query(Tool).filter(Tool.id == tool_id).first()
        if db_tool is None:
            return False  # Tool not found
        db.delete(db_tool)  # Delete tool
        db.commit()  # Commit transaction
        return True
    
    @staticmethod
    def check_out_tool(db: Session, tool_id: int, user_id: int):
        """
        Processes tool check-out by setting its availability to False.
        """
        db_tool = db.query(Tool).filter(Tool.id == tool_id, Tool.is_available == True).first()
        if not db_tool:
            return None  # Tool not available or not found

        db_tool.is_available = False
        db.commit()
        db.refresh(db_tool)
        return db_tool

    @staticmethod
    def return_tool(db: Session, tool_id: int, user_id: int):
        """
        Processes tool return by setting its availability to True.
        """
        db_tool = db.query(Tool).filter(Tool.id == tool_id, Tool.is_available == False).first()
        if not db_tool:
            return None  # Tool not checked out or not found

        db_tool.is_available = True
        db.commit()
        db.refresh(db_tool)
        return db_tool
    
    @staticmethod
    def update_tool_availability(db: Session, tool_id: int, is_available: bool):
        tool = db.query(Tool).filter(Tool.id == tool_id).first()
        if tool:
            tool.is_available = is_available
            db.commit()
            db.refresh(tool)
        return tool
    
    
    
    

    

    
