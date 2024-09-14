from pydantic import BaseModel, EmailStr
from enum import Enum

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True

        