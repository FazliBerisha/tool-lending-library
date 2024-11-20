from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tool import Tool
from app.models.reservation import Reservation
from app.models.user import User
from app.core.auth import get_current_user
from app.models.user import User


router = APIRouter()

@router.get("/usage", tags=["reporting"])
def get_usage_statistics( db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get basic usage statistics for administrators.

    Returns:
    - Total tools.
    - Total active reservations.
    - Total users.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    total_tools = db.query(Tool).count()
    active_reservations = db.query(Reservation).filter(Reservation.is_active == True).count()
    total_users = db.query(User).count()

    return {
        "total_tools": total_tools,
        "active_reservations": active_reservations,
        "total_users": total_users
    }