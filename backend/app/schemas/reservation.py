from pydantic import BaseModel
from datetime import datetime

class ReservationCreate(BaseModel):
    tool_id: int
    user_id: int

class ReservationReturn(BaseModel):
    reservation_id: int

class Reservation(BaseModel):
    id: int
    tool_id: int
    user_id: int
    reservation_date: datetime
    return_date: datetime | None

    class Config:
        orm_mode = True