from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# ============ USER SCHEMAS ============

class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username")

class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=6, description="Password (min 6 characters)")

class UserResponse(UserBase):
    """Schema for user data in API responses"""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        # Allow Pydantic to work with SQLAlchemy models
        from_attributes = True

# ============ TODO SCHEMAS ============

class TodoBase(BaseModel):
    """Base todo schema with common fields"""
    title: str = Field(..., min_length=1, max_length=200, description="Todo title")
    description: Optional[str] = Field(None, max_length=1000, description="Todo description")

class TodoCreate(TodoBase):
    """Schema for creating new todos"""
    pass  # Inherits all fields from TodoBase

class TodoUpdate(BaseModel):
    """Schema for updating existing todos"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None

class TodoResponse(TodoBase):
    """Schema for todo data in API responses"""
    id: int
    completed: bool
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class TodoWithOwner(TodoResponse):
    """Todo response with owner information"""
    owner: UserResponse

# ============ AUTH SCHEMAS ============

class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Data stored in JWT token"""
    username: Optional[str] = None

# ============ API RESPONSE SCHEMAS ============

class Message(BaseModel):
    """Generic message response"""
    message: str

class TodoListResponse(BaseModel):
    """Paginated todo list response"""
    todos: List[TodoResponse]
    total: int
    page: int
    per_page: int