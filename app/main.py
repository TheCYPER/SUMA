from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import auth, courses, tasks, calendar, ai, files

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="SUMA LMS API",
    description="Next-Generation Learning Management System API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure this properly for production
)

# Include routers
app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(tasks.router)
app.include_router(calendar.router)
app.include_router(ai.router)
app.include_router(files.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to SUMA LMS API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "SUMA LMS API is running"}


# Global exception handler
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"detail": "Resource not found"}


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"detail": "Internal server error"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
