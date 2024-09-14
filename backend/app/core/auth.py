"""
This module provides essential security utilities, including password hashing, verification, and JWT token generation.

Key Components:
- `pwd_context`: Configures `passlib` to use the bcrypt algorithm for secure password hashing and verification.

Functions:
- `hash_password(password: str)`: 
  - Hashes a plain text password using bcrypt.
  - Returns the hashed password.
  
- `verify_password(plain_password: str, hashed_password: str)`:
  - Compares a plain text password with its hashed equivalent.
  - Returns a boolean indicating whether they match.
  
- `create_access_token(data: dict, role: str)`:
  - Generates a JWT access token that includes the user’s data and role.
  - The token has an expiration time determined by `ACCESS_TOKEN_EXPIRE_MINUTES`.
  - It is encoded using the application’s secret key (`SECRET_KEY`) and a specified algorithm (`ALGORITHM`).
"""


from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, role: str):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "role": role})  # Include user's role in the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

