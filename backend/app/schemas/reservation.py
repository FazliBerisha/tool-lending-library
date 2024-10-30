from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class ReservationBase(BaseModel):
    tool_id: int
    start_date: datetime
    end_date: datetime

    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    user_id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
