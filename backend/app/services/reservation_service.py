from sqlalchemy.orm import Session
from app.models.reservation import Reservation
from app.models.tool import Tool
from app.schemas.reservation import ReservationCreate
from fastapi import HTTPException
from datetime import datetime

class ReservationService:
    @staticmethod
    def reserve_tool(db: Session, reservation: ReservationCreate):
        tool = db.query(Tool).filter(Tool.id == reservation.tool_id).first()
        if not tool:
            raise HTTPException(status_code=404, detail="Tool not found")
        if not tool.is_available:
            raise HTTPException(status_code=400, detail="Tool is not available")

        new_reservation = Reservation(tool_id=reservation.tool_id, user_id=reservation.user_id)
        tool.is_available = False
        db.add(new_reservation)
        db.commit()
        db.refresh(new_reservation)
        return new_reservation

    @staticmethod
    def return_tool(db: Session, reservation_id: int):
        reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")
        if reservation.return_date:
            raise HTTPException(status_code=400, detail="Tool already returned")

        reservation.return_date = datetime.utcnow()
        reservation.tool.is_available = True
        db.commit()
        db.refresh(reservation)
        return reservation