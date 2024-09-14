"""
This module provides utility functions for password hashing, verification, and JWT token creation.

Key Components:
- `pwd_context`: Uses `passlib` to define password hashing and verification methods with the bcrypt algorithm.
  
Functions:
- `hash_password(password: str)`: Hashes a plain text password using bcrypt and returns the hashed password.
  
- `verify_password(plain_password: str, hashed_password: str)`: Verifies if the plain text password matches the hashed password.
  
- `create_access_token(data: dict, role: str)`: 
  - Creates a JWT access token containing the user's data and role.
  - The token includes an expiration time (`exp`) set based on `ACCESS_TOKEN_EXPIRE_MINUTES`.
  - Encodes the token using the secret key (`SECRET_KEY`) and specified algorithm (`ALGORITHM`).
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

