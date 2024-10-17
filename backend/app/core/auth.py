"""
This module provides security utilities for password hashing, verification, and JWT token generation.

Components:
- `pwd_context`: Configures `passlib` to use bcrypt for password hashing.
- `hash_password`: Hashes passwords.
- `verify_password`: Compares plain text passwords with hashed ones.
- `create_access_token`: Generates JWT tokens with embedded user roles.
- `get_current_user_role`: Extracts the user's role from the JWT token.
- `get_current_user`: Retrieves the current user based on the JWT token.
"""

from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models.user import User

# Secret key and algorithm for JWT encoding, loaded from settings.
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

def create_access_token(data: dict, role: str):
    """
    Generates a JWT token with user data, role, and expiration.

    Args:
    - data (dict): Information to include in the token.
    - role (str): User role to be embedded in the token.
    
    Returns:
    - str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "role": role})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user_role(token: str):
    """
    Extracts and returns the user's role from the JWT token.

    Args:
    - token (str): JWT token.

    Returns:
    - str: User role from the token.

    Raises:
    - HTTPException: If the role is missing or the token is invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role = payload.get("role")
        
        if role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Role not found in token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return role
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Retrieves the current user based on the JWT token.

    Args:
    - token (str): JWT token.
    - db (Session): Database session.

    Returns:
    - User: Current user object.

    Raises:
    - HTTPException: If the user is not found or the token is invalid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
