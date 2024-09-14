"""
Database connection and session management for SQLAlchemy.
- Configures the SQLAlchemy engine and session maker.
- Provides a dependency for managing database sessions in FastAPI routes.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL for SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Create the SQLAlchemy engine for connecting to the database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a configured "Session" class to be used for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

def get_db():
    """
    Dependency function for obtaining a database session.
    - Yields a database session for the duration of a request.
    - Ensures that the session is closed after use to prevent leaks.
    :return: A database session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
