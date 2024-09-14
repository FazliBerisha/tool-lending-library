# app/schemas/user.py
"""
Pydantic schemas for User-related operations.
- Defines UserBase, UserCreate, and User schemas
- Used for request/response models in API
"""

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True