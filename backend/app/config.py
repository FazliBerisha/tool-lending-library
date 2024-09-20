"""
Configuration settings for the application.

This module defines various configuration settings needed for the application. It includes settings 
for the database connection, JWT authentication, and other application-wide parameters. The settings 
are loaded from environment variables using the Pydantic `BaseSettings` class, allowing for a flexible 
and secure configuration management approach.

Settings include:
- `DATABASE_URL`: The URL for the database connection.
- `SECRET_KEY`: The secret key used for JWT encoding and decoding.
- `ALGORITHM`: The algorithm used for JWT encoding.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: The expiration time for access tokens, in minutes.
- `VALID_ROLES`: The list of valid user roles in the application.
- `PROJECT_NAME`: The name of the project.

The `Config` class within `Settings` specifies the location of the environment file.
"""

from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    The `Settings` class inherits from `BaseSettings` and uses Pydantic to parse and validate settings 
    from environment variables. Default values are provided where appropriate.
    """
    DATABASE_URL: str = "sqlite:///./sql_app.db"  # Database connection URL
    SECRET_KEY: str = "your-secret-key-here"  # Secret key for JWT encoding/decoding (replace with a secure key)
    ALGORITHM: str = "HS256"  # Algorithm used for JWT encoding
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Token expiration time in minutes
    VALID_ROLES: List[str] = ["user", "admin"]  # List of valid user roles
    PROJECT_NAME: str = "Tool Lending Library"  # Name of the project

    class Config:
        """
        Configuration for loading environment variables.
        
        The `Config` class specifies the path to the environment file. This allows Pydantic to load
        environment variables from a `.env` file.
        """
        env_file = ".env"

# Create an instance of the Settings class to access the settings
settings = Settings()

# Export VALID_ROLES for use in other parts of the application
VALID_ROLES = settings.VALID_ROLES

