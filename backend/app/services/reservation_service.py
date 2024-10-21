from sqlalchemy.orm import Session
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate

class ReservationService:

    @staticmethod
    def create_reservation(db: Session, reservation_data: ReservationCreate, user_id: int):
        db_reservation = Reservation(
            tool_id=reservation_data.tool_id,
            user_id=user_id,
            reservation_date=reservation_data.reservation_date
        )
        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation)
        return db_reservation

    @staticmethod
    def cancel_reservation(db: Session, reservation_id: int, user_id: int):
        reservation = db.query(Reservation).filter(
            Reservation.id == reservation_id,
            Reservation.user_id == user_id
        ).first()
        if reservation:
            db.delete(reservation)
            db.commit()
            return True
        return False

    @staticmethod
    def get_active_reservation(db: Session, tool_id: int, user_id: int):
        return db.query(Reservation).filter(
            Reservation.tool_id == tool_id,
            Reservation.user_id == user_id,
            Reservation.is_active == True
        ).first()
