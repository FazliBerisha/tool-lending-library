# app/main.py
"""
Main entry point for the FastAPI application.
- Initializes the FastAPI app
- Includes routers for different parts of the application (users and tools)
- Sets up database tables
"""

from fastapi import FastAPI
from app.routers import user, tool  # Add import for tool router
from app.database import engine
from app.models import user as user_model, tool as tool_model  # Add import for tool model

# Create tables for both user and tool models
user_model.Base.metadata.create_all(bind=engine)
tool_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
app.include_router(tool.router, prefix="/api/v1/tools", tags=["tools"])