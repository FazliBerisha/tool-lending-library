from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.reservation import Reservation
from app.models.tool import Tool

class ReportService:
    @staticmethod
    def most_borrowed_tools(db: Session, limit: int = 5):
        """
        Retrieves the most borrowed tools.

        Args:
            db (Session): The database session.
            limit (int): The maximum number of tools to return.

        Returns:
            List[dict]: A list of dictionaries containing tool name and borrow count.
        """
        results = (
            db.query(Tool.name, func.count(Reservation.id).label("borrow_count"))
            .join(Reservation, Tool.id == Reservation.tool_id)
            .filter(Reservation.is_active == False)  # Only count completed reservations
            .group_by(Tool.name)
            .order_by(func.count(Reservation.id).desc())
            .limit(limit)
            .all()
        )
        return [{"tool_name": result[0], "borrow_count": result[1]} for result in results]
    
    @staticmethod
    def least_borrowed_tools(db: Session, limit: int = 5):
        """
        Retrieves the least borrowed tools.

        Args:
            db (Session): The database session.
            limit (int): The maximum number of tools to return.

        Returns:
            List[dict]: A list of dictionaries containing tool name and borrow count.
        """
        results = (
            db.query(Tool.name, func.count(Reservation.id).label("borrow_count"))
            .join(Reservation, Tool.id == Reservation.tool_id)
            .filter(Reservation.is_active == False)  # Only count completed reservations
            .group_by(Tool.name)
            .order_by(func.count(Reservation.id).asc())  # Ascending order for least borrowed
            .limit(limit)
            .all()
        )
        return [{"tool_name": result[0], "borrow_count": result[1]} for result in results]
