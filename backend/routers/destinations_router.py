from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..auth import get_current_user
from ..models import User, Destination
from ..schemas import DestinationResponse, DestinationSearchRequest, DestinationSearchResponse

router = APIRouter()

@router.get("/search", response_model=List[DestinationSearchResponse])
async def search_destinations(
    query: str,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search for destinations"""
    destinations = db.query(Destination).filter(
        Destination.name.ilike(f"%{query}%") | 
        Destination.country.ilike(f"%{query}%") |
        Destination.city.ilike(f"%{query}%")
    ).limit(limit).all()
    
    return [
        DestinationSearchResponse(
            name=dest.name,
            country=dest.country,
            city=dest.city,
            description=dest.description,
            image_url=dest.image_url,
            average_budget=dest.average_budget_per_day,
            best_time_to_visit=dest.best_time_to_visit
        )
        for dest in destinations
    ]

@router.get("/popular", response_model=List[DestinationResponse])
async def get_popular_destinations(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get popular destinations"""
    destinations = db.query(Destination).order_by(Destination.tourist_rating.desc()).limit(limit).all()
    
    return [
        DestinationResponse(
            id=dest.id,
            name=dest.name,
            country=dest.country,
            city=dest.city,
            latitude=dest.latitude,
            longitude=dest.longitude,
            description=dest.description,
            best_time_to_visit=dest.best_time_to_visit,
            average_budget_per_day=dest.average_budget_per_day,
            safety_rating=dest.safety_rating,
            tourist_rating=dest.tourist_rating,
            image_url=dest.image_url,
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
        best_time_to_visit=destination.best_time_to_visit,
        average_budget_per_day=destination.average_budget_per_day,
        safety_rating=destination.safety_rating,
        tourist_rating=destination.tourist_rating,
        image_url=destination.image_url,
        weather_info=destination.weather_info or {},
        attractions=destination.attractions or [],
        local_cuisine=destination.local_cuisine or [],
        created_at=destination.created_at
    )