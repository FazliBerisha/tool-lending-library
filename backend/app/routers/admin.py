from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app.models.tool import Tool
from app.models.reservation import Reservation
from app.models.user import User
from app.core.auth import get_current_user

router = APIRouter()

@router.get("/stats", tags=["admin"])
def get_admin_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get comprehensive statistics for admin dashboard."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    # Basic stats
    total_tools = db.query(Tool).count()
    active_reservations = db.query(Reservation).filter(Reservation.is_active == True).count()
    total_users = db.query(User).count()

    # Tool availability stats
    available_tools = db.query(Tool).filter(Tool.is_available == True).count()
    checked_out_tools = total_tools - available_tools

    # Reservation stats for last 30 days
    thirty_days_ago = datetime.now() - timedelta(days=30)
    monthly_reservations = (
        db.query(Reservation)
        .filter(Reservation.reservation_date >= thirty_days_ago)
        .count()
    )

    # Most active users
    active_users = (
        db.query(
            User.username,
            func.count(Reservation.id).label('reservation_count')
        )
        .join(Reservation)
        .group_by(User.username)
        .order_by(func.count(Reservation.id).desc())
        .limit(5)
        .all()
    )

    return {
        "total_tools": total_tools,
        "active_reservations": active_reservations,
        "total_users": total_users,
        "tool_stats": {
            "available": available_tools,
            "checked_out": checked_out_tools
        },
        "monthly_reservations": monthly_reservations,
        "active_users": [
            {"username": username, "reservations": count}
            for username, count in active_users
        ]
    }