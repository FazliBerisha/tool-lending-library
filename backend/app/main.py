"""
Main entry point for the FastAPI application.

This module initializes the FastAPI application and sets up the various components required for the
application to function, including routers and database tables. It is responsible for configuring
the app, including its title, and incorporating different routers for handling various parts of the
application such as user management, tool management, and authentication.

Components:
- `create_tables()`: Function to create database tables based on the model metadata.
- `app`: Instance of the FastAPI application.
- Routers: 
  - `auth.auth_router`: Handles authentication-related routes.
  - `user.router`: Manages user-related routes.
  - `tool.router`: Manages tool-related routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, tool, auth, reservation
from app.config import settings
from app.database import create_tables


# Create tables for all models
create_tables()

# Initialize the FastAPI application with a title from settings
app = FastAPI(title=settings.PROJECT_NAME)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from your React app
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include the routers for various parts of the application
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
app.include_router(tool.router, prefix="/api/v1/tools", tags=["tools"])
app.include_router(reservation.router, prefix="/api/v1/reservations", tags=["reservation"]) 
