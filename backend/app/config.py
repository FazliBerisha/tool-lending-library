"""
Configuration settings for the application.
- Defines database URL
- Sets up JWT secret key and algorithm
- Configures other app-wide settings
"""

DATABASE_URL = "sqlite:///./test.db"
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
