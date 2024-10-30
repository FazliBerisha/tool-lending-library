from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.reservation_service import ReservationService
from app.schemas.reservation import Reservation, ReservationCreate
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=Reservation)
def create_reservation(
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ReservationService.create_reservation(db, reservation, current_user.id)

@router.get("/user/", response_model=List[Reservation])
def get_user_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ReservationService.get_user_reservations(db, current_user.id)

@router.get("/tool/{tool_id}", response_model=List[Reservation])
def get_tool_reservations(
    tool_id: int,
    db: Session = Depends(get_db)
):
    return ReservationService.get_tool_reservations(db, tool_id)
