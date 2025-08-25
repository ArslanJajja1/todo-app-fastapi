from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import verify_token
from app.models import User

# OAuth2 scheme for JWT tokens
# tokenUrl points to our login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from JWT token.
    
    This dependency:
    1. Extracts JWT token from Authorization header
    2. Verifies the token
    3. Looks up the user in database
    4. Returns the user object
    
    Raises HTTPException if:
    - Token is invalid
    - Token is expired
    - User doesn't exist
    """
    
    # Create credentials exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verify token and get username
    username = verify_token(token)
    if username is None:
        raise credentials_exception
    
    # Look up user in database
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
        
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current user and ensure they are active.
    
    Args:
        current_user: User from get_current_user dependency
        
    Returns:
        Active user object
        
    Raises:
        HTTPException if user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user