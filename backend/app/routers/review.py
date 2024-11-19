from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.review_service import ReportService
from app.core.deps import get_current_user_role

router = APIRouter()

@router.get("/most-borrowed-tools", tags=["reports"])
def get_most_borrowed_tools(limit: int = 5, db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can access this report."
        )
    return ReportService.get_most_borrowed_tools(db, limit=limit)

@router.get("/least-borrowed-tools", tags=["reports"])
def get_least_borrowed_tools(
    limit: int = 5, 
    db: Session = Depends(get_db), 
    role: str = Depends(get_current_user_role)
):
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can access this report."
        )
    return ReportService.get_least_borrowed_tools(db, limit=limit)
