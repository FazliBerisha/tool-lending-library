"""
Pydantic schemas for handling user-related operations.

Schemas:
- `UserBase`: Base schema with common user attributes (email).
- `UserCreate`: Extends `UserBase`, used for creating a new user, includes password and optional username and role.
- `UserInDB`: Schema for the user as stored in the database, includes hashed password and user status.
- `User`: Response model for returning user information, excluding sensitive data like password.
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
    - Extends `UserBase`, adding `password`, optional `username`, and `role` (default is 'user').
    """
    password: str
    username: str | None = None  # Optional username
    role: str = "user"  # Default role is 'user'

class UserInDB(UserBase):
    """
    Schema for the user object as it is stored in the database.
    - Includes the hashed password and `is_active` status, along with the user's ID.
    """
    id: int
    username: str | None = None  # Optional username
    hashed_password: str
    is_active: bool = True  # Default is active

class User(UserBase):
    """
    Response schema for returning user information to the client.
    - Excludes the password, but includes the user's ID, `is_active` status, and role.
    - Enables ORM mode for compatibility with SQLAlchemy models.
    """
    id: int
    username: str | None = None
    is_active: bool = True  # Default is active
    role: str  # User's role (e.g., 'user', 'admin')
    full_name: str | None = None
    bio: str | None = None
    location: str | None = None
    profile_picture: str | None = None

    class Config:
        orm_mode = True  # Allows ORM objects to be returned as response models

class UserProfileUpdate(BaseModel):
    full_name: str | None = None
    bio: str | None = None
    location: str | None = None
    profile_picture: str | None = None