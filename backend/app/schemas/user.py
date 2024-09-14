# app/schemas/user.py
"""
Pydantic schemas for User-related operations.
- Defines UserBase, UserCreate, and User schemas
- Used for request/response models in API
"""

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    username: str | None = None  # Make username optional

class UserInDB(UserBase):
    id: int
    username: str | None = None
    hashed_password: str
    is_active: bool = True

class User(UserBase):
    id: int
    username: str | None = None
    is_active: bool = True

    class Config:
        orm_mode = True