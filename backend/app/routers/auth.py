from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import create_user, get_user_by_username
from app.core.auth import verify_password, create_access_token

auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@auth_router.post("/register")
def register_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    user = create_user(db, username, email, password)
    return {"msg": "User registered successfully"}

@auth_router.post("/login")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username, "role": user.role.value}) # added role to the payload
    return {"access_token": access_token, "token_type": "bearer"}

#Anna
def role_required(required_role: str):
    def role_checker(token: str = Depends(oauth2_scheme)):
        # Decode the JWT token
        payload = decode_jwt(token)
        username: str = payload.get("sub")
        # Check if the username is present in the token payload
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        # Get the user from the database
        user = get_user_by_username(db, username)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        
        # Check if the user's role matches the required role
        if user.role != required_role:
            raise HTTPException(status_code=403, detail="Access denied")
        return user
    return role_checker

