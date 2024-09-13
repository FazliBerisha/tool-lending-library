from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import create_user, get_user_by_username
from app.core.auth import verify_password, create_access_token

auth_router = APIRouter()

@auth_router.post("/register")
def register_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    user = create_user(db, username, email, password)
    return {"msg": "User registered successfully"}

@auth_router.post("/login")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}