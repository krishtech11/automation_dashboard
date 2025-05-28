from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from .config import settings
from .api.endpoints import web, desktop, document

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="An all-in-one automation dashboard API for web, desktop, and document automation",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API routers
app.include_router(web.router, prefix="/api", tags=["web"])
app.include_router(desktop.router, prefix="/api", tags=["desktop"])
app.include_router(document.router, prefix="/api", tags=["document"])

@app.get("/")
async def root():
    """Root endpoint that provides information about the API."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "endpoints": [
            {"path": "/api/web-automate", "method": "POST", "description": "Web automation endpoint"},
            {"path": "/api/desktop-automate", "method": "POST", "description": "Desktop automation endpoint"},
            {"path": "/api/document/extract-text", "method": "POST", "description": "Document text extraction endpoint"}
        ]
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1
    )
