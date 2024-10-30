from typing import Optional
from pydantic import BaseModel
from datetime import date
from app.schemas.tool import Tool

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
    is_checked_out: bool
    tool: Tool

    class Config:
        orm_mode = True
