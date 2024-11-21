from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tool import Tool
from app.models.user import User
from app.core.auth import get_current_user

router = APIRouter()

# This file will be used for tool review functionality in the future