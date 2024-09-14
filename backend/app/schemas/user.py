"""
Pydantic schemas for handling user-related operations.
- `UserBase`: Base schema for common user attributes.
- `UserCreate`: Extends `UserBase`, used for creating a new user.
- `UserInDB`: Schema for the user as stored in the database, includes hashed password.
- `User`: Response model for returning user information, excludes password.
"""

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """
    Base schema with common fields for user data.
    - Includes `email` as a required field with email validation.
    """
    email: EmailStr

class UserCreate(UserBase):
    """
    Schema for user creation requests.
    - Extends `UserBase`, adding `password` and optional `username`.
    """
    password: str
    username: str | None = None  # Username is optional

class UserInDB(UserBase):
    """
    Schema for the user object as it is stored in the database.
    - Includes the hashed password and `is_active` status.
    """
    id: int
    username: str | None = None
    hashed_password: str
    is_active: bool = True

class User(UserBase):
    """
    Response schema for returning user information.
    - Excludes the password, but includes the user's ID and `is_active` status.
    - Enables ORM mode to support SQLAlchemy models.
    """
    id: int
    username: str | None = None
    is_active: bool = True

    class Config:
        orm_mode = True
