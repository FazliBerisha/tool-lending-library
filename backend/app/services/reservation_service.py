from sqlalchemy.orm import Session
from datetime import datetime
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate
from fastapi import HTTPException

class ReservationService:
    @staticmethod
    def create_reservation(db: Session, reservation: ReservationCreate, user_id: int):
        # Check if tool is available for the requested dates
        existing_reservation = db.query(Reservation).filter(
            Reservation.tool_id == reservation.tool_id,
            Reservation.status != "rejected",
            ((Reservation.start_date <= reservation.start_date) & 
             (Reservation.end_date >= reservation.start_date)) |
            ((Reservation.start_date <= reservation.end_date) & 
             (Reservation.end_date >= reservation.end_date))
        ).first()

        if existing_reservation:
            raise HTTPException(
                status_code=400,
                detail="Tool is not available for the selected dates"
            )

        db_reservation = Reservation(
            **reservation.dict(),
            user_id=user_id,
            status="pending"
        )
        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation)
        return db_reservation

    @staticmethod
    def get_user_reservations(db: Session, user_id: int):
        return db.query(Reservation).filter(Reservation.user_id == user_id).all()

    @staticmethod
    def get_tool_reservations(db: Session, tool_id: int):
        return db.query(Reservation).filter(Reservation.tool_id == tool_id).all()

    @staticmethod
    def update_reservation_status(db: Session, reservation_id: int, status: str):
        reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")
        
        reservation.status = status
        db.commit()
        db.refresh(reservation)
        return reservation
