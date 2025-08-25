from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Todo, User
from app.schemas import TodoCreate, TodoUpdate, TodoResponse, TodoListResponse
from app.dependencies import get_current_active_user
from app.schemas import Message

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

@router.get("", response_model=TodoListResponse)
def get_todos(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get user's todos with pagination and filtering.
    
    Args:
        page: Page number (starts from 1)
        per_page: Number of items per page (max 100)
        completed: Filter by completion status (optional)
        search: Search term for title/description (optional)
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Paginated list of todos
    """
    
    # Base query - only user's todos
    query = db.query(Todo).filter(Todo.owner_id == current_user.id)
    
    # Apply filters
    if completed is not None:
        query = query.filter(Todo.completed == completed)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Todo.title.ilike(search_term)) | 
            (Todo.description.ilike(search_term))
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * per_page
    todos = query.offset(offset).limit(per_page).all()
    
    return TodoListResponse(
        todos=todos,
        total=total,
        page=page,
        per_page=per_page
    )

@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new todo item.
    
    Args:
        todo_data: Todo creation data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created todo item
    """
    
    # Create new todo
    db_todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        owner_id=current_user.id
    )
    
    # Save to database
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    
    return db_todo

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific todo by ID.
    
    Args:
        todo_id: Todo ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Todo item
        
    Raises:
        HTTPException 404: If todo not found or doesn't belong to user
    """
    
    # Find todo
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.owner_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    return todo

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a todo item.
    
    Args:
        todo_id: Todo ID
        todo_update: Todo update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated todo item
        
    Raises:
        HTTPException 404: If todo not found or doesn't belong to user
    """
    
    # Find todo
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.owner_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    # Update fields that were provided
    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)
    
    # Save changes
    db.commit()
    db.refresh(todo)
    
    return todo

@router.delete("/{todo_id}", response_model=Message)
def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a todo item.
    
    Args:
        todo_id: Todo ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException 404: If todo not found or doesn't belong to user
    """
    
    # Find todo
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.owner_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    # Delete todo
    db.delete(todo)
    db.commit()
    
    return Message(message="Todo deleted successfully")

@router.post("/{todo_id}/toggle", response_model=TodoResponse)
def toggle_todo_completion(
    todo_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Toggle todo completion status.
    
    Args:
        todo_id: Todo ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated todo item
        
    Raises:
        HTTPException 404: If todo not found or doesn't belong to user
    """
    
    # Find todo
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.owner_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    # Toggle completion
    todo.completed = not todo.completed
    
    # Save changes
    db.commit()
    db.refresh(todo)
    
    return todo