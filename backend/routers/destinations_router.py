from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..auth import get_current_user
from ..models import User, Destination
from ..schemas import DestinationResponse, LocationSearchRequest, LocationResponse

router = APIRouter()

@router.get("/search", response_model=List[LocationResponse])
async def search_destinations(
    query: str,
    limit: int = 10,
    current_user: User = Depends(get_current_user)
):
    """Search for destinations"""
    # Mock destination search
    destinations = [
        {
            "name": "Paris",
            "country": "France",
            "city": "Paris",
            "latitude": 48.8566,
            "longitude": 2.3522,
            "description": "The City of Light",
            "best_time_to_visit": "April to June, September to October",
            "average_budget": 150.0
        },
        {
            "name": "Tokyo",
            "country": "Japan", 
            "city": "Tokyo",
            "latitude": 35.6762,
            "longitude": 139.6503,
            "description": "Modern metropolis with traditional culture",
            "best_time_to_visit": "March to May, September to November",
            "average_budget": 200.0
        },
        {
            "name": "Bali",
            "country": "Indonesia",
            "city": "Denpasar",
            "latitude": -8.3405,
            "longitude": 115.0920,
            "description": "Tropical paradise with rich culture",
            "best_time_to_visit": "April to October",
            "average_budget": 80.0
        }
    ]
    
    # Filter based on query
    filtered = [d for d in destinations if query.lower() in d["name"].lower()]
    
    return [LocationResponse(**dest) for dest in filtered[:limit]]

@router.get("/popular", response_model=List[DestinationResponse])
async def get_popular_destinations(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get popular destinations"""
    destinations = db.query(Destination).limit(limit).all()
    
    return [
        DestinationResponse(
            id=dest.id,
            name=dest.name,
            country=dest.country,
            city=dest.city,
            latitude=dest.latitude,
            longitude=dest.longitude,
            description=dest.description,
            weather_info=dest.weather_info or {},
            attractions=dest.attractions or [],
            local_cuisine=dest.local_cuisine or [],
            created_at=dest.created_at
        )
        for dest in destinations
    ]

@router.get("/{destination_id}", response_model=DestinationResponse)
async def get_destination(
    destination_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get destination details"""
    destination = db.query(Destination).filter(Destination.id == destination_id).first()
    
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )
    
    return DestinationResponse(
        id=destination.id,
        name=destination.name,
        country=destination.country,
        city=destination.city,
        latitude=destination.latitude,
        longitude=destination.longitude,
        description=destination.description,
        weather_info=destination.weather_info or {},
        attractions=destination.attractions or [],
        local_cuisine=destination.local_cuisine or [],
        created_at=destination.created_at
    )