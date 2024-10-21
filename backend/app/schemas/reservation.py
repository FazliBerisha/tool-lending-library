from typing import Optional
from pydantic import BaseModel
from datetime import date

class ReservationBase(BaseModel):
    tool_id: int
    reservation_date: date

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    user_id: int
    return_date: Optional[date]
    is_active: bool

    class Config:
        orm_mode = True
