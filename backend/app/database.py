from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.config import settings

# Create the SQLAlchemy engine for connecting to the database
# The engine uses the database URL from the settings and a static connection pool.
# StaticPool is suitable for single-threaded applications or tests.
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite to allow usage across threads
    poolclass=StaticPool  # StaticPool is used here to avoid creating multiple connections
)

# Create a configured "Session" class to be used for creating database sessions
# This session factory handles the transactions and queries for the application.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all SQLAlchemy declarative models
# This class maintains the metadata for all models and provides a base class for model definitions.
Base = declarative_base()

def create_tables():
    """
    Create all tables in the database based on the metadata of the declarative models.

    This function uses the `Base.metadata.create_all` method to generate the database schema.
    It ensures that all defined models have corresponding tables created in the database.
    """
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Dependency function to provide a database session.

    Yields:
        Session: A SQLAlchemy session instance used for interacting with the database.
    
    This function is designed to be used as a dependency in FastAPI routes to ensure that 
    each request gets a new session and that the session is properly closed after the request.
    """
    db = SessionLocal()
    try:
        yield db  # Provide the session to the request
    finally:
        db.close()  # Ensure the session is closed after use
