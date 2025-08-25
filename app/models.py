from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    """
    User table - stores user account information
    
    Relationships:
    - One user can have many todos (one-to-many)
    """
    __tablename__ = "users"  # Table name in database
    
    # Primary key - unique identifier for each user
    id = Column(Integer, primary_key=True, index=True)
    
    # User credentials
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # User status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship: One user has many todos
    todos = relationship("Todo", back_populates="owner", cascade="all, delete-orphan")

class Todo(Base):
    """
    Todo table - stores todo items
    
    Relationships:
    - Each todo belongs to one user (many-to-one)
    """
    __tablename__ = "todos"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Todo content
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    
    # Foreign key - links to User table
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship: Each todo belongs to one user
    owner = relationship("User", back_populates="todos")