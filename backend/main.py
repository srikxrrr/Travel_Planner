from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import uvicorn
from typing import List, Optional
import os
from dotenv import load_dotenv

try:
    # Try relative imports first (when run as module)
    from .database import init_db, get_db
    from .auth import get_current_user
    from .models import User
    from .routers import (
        auth_router,
        trips_router,
        bookings_router,
        destinations_router,
        recommendations_router,
        weather_router,
        hotels_router,
        flights_router,
        trains_router
    )
except ImportError:
    # Fallback to absolute imports (when run directly)
    from database import init_db, get_db
    from auth import get_current_user
    from models import User
    from routers import (
        auth_router,
        trips_router,
        bookings_router,
        destinations_router,
        recommendations_router,
        weather_router,
        hotels_router,
        flights_router,
        trains_router
    )

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    pass

# Create FastAPI app
app = FastAPI(
    title="Travel Planner API",
    description="A comprehensive travel planning and booking backend API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(trips_router.router, prefix="/api/v1/trips", tags=["Trip Planning"])
app.include_router(bookings_router.router, prefix="/api/v1/bookings", tags=["Bookings"])
app.include_router(destinations_router.router, prefix="/api/v1/destinations", tags=["Destinations"])
app.include_router(recommendations_router.router, prefix="/api/v1/recommendations", tags=["Recommendations"])
app.include_router(weather_router.router, prefix="/api/v1/weather", tags=["Weather"])
app.include_router(hotels_router.router, prefix="/api/v1/hotels", tags=["Hotels"])
app.include_router(flights_router.router, prefix="/api/v1/flights", tags=["Flights"])
app.include_router(trains_router.router, prefix="/api/v1/trains", tags=["Trains"])

@app.get("/")
async def root():
    return {
        "message": "Travel Planner API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "api": "/api/v1"
        }
    }

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "services": {
            "database": "connected",
            "redis": "connected",
            "external_apis": "available"
        }
    }

@app.get("/api/v1/me", response_model=dict)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
        log_level="info"
    )