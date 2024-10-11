from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.reservation_service import ReservationService
from app.schemas.reservation import ReservationCreate, Reservation
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/reserve", response_model=Reservation)
def reserve_tool(reservation: ReservationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to reserve tools")
    return ReservationService.reserve_tool(db, reservation)

@router.post("/return/{reservation_id}", response_model=Reservation)
def return_tool(reservation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to return tools")
    return ReservationService.return_tool(db, reservation_id)