from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create database engine
# echo=True shows SQL queries in console (useful for debugging)
engine = create_engine(
    settings.database_url,
    echo=settings.debug  # Show SQL queries when debug=True
)

# Create session factory
# Sessions handle database transactions
SessionLocal = sessionmaker(
    autocommit=False,  # Don't auto-commit transactions
    autoflush=False,   # Don't auto-flush changes
    bind=engine        # Bind to our database engine
)

# Base class for all database models
Base = declarative_base()

def get_db():
    """
    Dependency function that provides database sessions.
    
    This function:
    1. Creates a new database session
    2. Yields it to the endpoint function
    3. Automatically closes it when done (even if error occurs)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()