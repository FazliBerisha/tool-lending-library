from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.auth import get_current_user_role
from app.database import get_db
from app.models.user import User

# OAuth2PasswordBearer retrieves the token from the Authorization header.
# `tokenUrl` is the endpoint where clients can obtain a token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Retrieves the current user based on the JWT token.

    Args:
    - token (str): JWT token from the Authorization header.
    - db (Session): Database session provided via FastAPI dependency.

    Returns:
    - User: The user corresponding to the role in the token.

    Raises:
    - HTTPException: If no user is found or the token is invalid (401 Unauthorized).
    """
    # Get the role from the token.
    role = get_current_user_role(token)
    
    # Query the database for a user with the matching role.
    user = db.query(User).filter(User.role == role).first()
    
    # Raise an exception if no user matches the role.
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    
    return user

def role_required(*required_roles: str):
    """
    Enforces role-based access control.

    Args:
    - *required_roles (str): List of roles authorized to access the resource.

    Returns:
    - function: A nested function that checks if the user's role is authorized.

    Raises:
    - HTTPException: If the user's role is unauthorized (403 Forbidden).
    """
    def role_checker(current_user: User = Depends(get_current_user)):
        # Check if the user's role matches any of the required roles.
        if current_user.role not in required_roles:
            # Raise a 403 error if the role is unauthorized.
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {', '.join(required_roles)}"
            )
    
    # Return the role checker function to use as a dependency.
    return role_checker
