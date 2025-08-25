from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import auth, todos

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="A professional Todo API with JWT authentication",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(todos.router)

# Root endpoint
@app.get("/")
def read_root():
    """
    Root endpoint - API health check.
    
    Returns:
        Welcome message and API status
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "status": "healthy",
        "docs": "/docs"
    }

# Health check endpoint
@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        API health status
    """
    return {"status": "healthy"}