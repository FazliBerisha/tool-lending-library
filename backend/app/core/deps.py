# core/dependencies.py

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.config import SECRET_KEY, ALGORITHM
from app.core.auth import get_current_user_role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def role_required(required_role: str):
    """
    Function to enforce role-based access control.
    - Ensures that only users with the required role can access certain API routes.
    
    Args:
    - required_role (str): The role that the user must have to access the route.
    
    Returns:
    - A function that checks if the user's role matches the required role.
    
    Raises:
    - HTTPException: If the user's role doesn't match the required role.
    """
    def role_checker(token: str = Depends(oauth2_scheme)):
        role = get_current_user_role(token)
        if role != required_role:
            raise HTTPException(status_code=403, detail=f"Insufficient permissions for role: {role}")
    return role_checker
