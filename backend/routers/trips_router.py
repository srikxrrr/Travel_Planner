from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import random

from ..database import get_db
from ..auth import get_current_user
from ..models import User, Trip, Destination, TripStatus
from ..schemas import TripCreate, TripResponse, DestinationResponse

router = APIRouter()

@router.post("/", response_model=TripResponse)
async def create_trip(
    trip_data: TripCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new trip"""
    
    # Check if destination exists
    destination = db.query(Destination).filter(Destination.id == trip_data.destination_id).first()
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )
    
    trip = Trip(
        user_id=current_user.id,
        destination_id=trip_data.destination_id,
        title=trip_data.title,
        description=trip_data.description,
        start_date=trip_data.start_date,
        end_date=trip_data.end_date,
        total_budget=trip_data.total_budget,
        travelers_count=trip_data.travelers_count,
        trip_type=trip_data.trip_type,
        accommodation_preference=trip_data.accommodation_preference,
        interests=trip_data.interests,
        pace=trip_data.pace,
        special_requests=trip_data.special_requests,
        status=TripStatus.PLANNING,
        itinerary={},
        ai_generated=False
    )
    
    db.add(trip)
    db.commit()
    db.refresh(trip)
    
    # Load destination for response
    destination_response = DestinationResponse(
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
    
    return TripResponse(
        id=trip.id,
        user_id=trip.user_id,
        destination_id=trip.destination_id,
        title=trip.title,
        description=trip.description,
        start_date=trip.start_date,
        end_date=trip.end_date,
        total_budget=trip.total_budget,
        spent_amount=trip.spent_amount,
        travelers_count=trip.travelers_count,
        trip_type=trip.trip_type,
        accommodation_preference=trip.accommodation_preference,
        interests=trip.interests,
        pace=trip.pace,
        special_requests=trip.special_requests,
        status=trip.status,
        itinerary=trip.itinerary,
        ai_generated=trip.ai_generated,
        created_at=trip.created_at,
        destination=destination_response
    )

@router.get("/", response_model=List[TripResponse])
async def get_my_trips(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all trips for the current user"""
    trips = db.query(Trip).filter(Trip.user_id == current_user.id).all()
    
    trip_responses = []
    for trip in trips:
        destination = db.query(Destination).filter(Destination.id == trip.destination_id).first()
        destination_response = None
        
        if destination:
            destination_response = DestinationResponse(
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
        
        trip_responses.append(TripResponse(
            id=trip.id,
            user_id=trip.user_id,
            destination_id=trip.destination_id,
            title=trip.title,
            description=trip.description,
            start_date=trip.start_date,
            end_date=trip.end_date,
            total_budget=trip.total_budget,
            spent_amount=trip.spent_amount,
            travelers_count=trip.travelers_count,
            trip_type=trip.trip_type,
            accommodation_preference=trip.accommodation_preference,
            interests=trip.interests,
            pace=trip.pace,
            special_requests=trip.special_requests,
            status=trip.status,
            itinerary=trip.itinerary,
            ai_generated=trip.ai_generated,
            created_at=trip.created_at,
            destination=destination_response
        ))
    
    return trip_responses

@router.get("/{trip_id}", response_model=TripResponse)
async def get_trip(
    trip_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific trip"""
    trip = db.query(Trip).filter(
        Trip.id == trip_id,
        Trip.user_id == current_user.id
    ).first()
    
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )
    
    destination = db.query(Destination).filter(Destination.id == trip.destination_id).first()
    destination_response = None
    
    if destination:
        destination_response = DestinationResponse(
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
    
    return TripResponse(
        id=trip.id,
        user_id=trip.user_id,
        destination_id=trip.destination_id,
        title=trip.title,
        description=trip.description,
        start_date=trip.start_date,
        end_date=trip.end_date,
        total_budget=trip.total_budget,
        spent_amount=trip.spent_amount,
        travelers_count=trip.travelers_count,
        trip_type=trip.trip_type,
        accommodation_preference=trip.accommodation_preference,
        interests=trip.interests,
        pace=trip.pace,
        special_requests=trip.special_requests,
        status=trip.status,
        itinerary=trip.itinerary,
        ai_generated=trip.ai_generated,
        created_at=trip.created_at,
        destination=destination_response
    )

@router.delete("/{trip_id}")
async def delete_trip(
    trip_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a trip"""
    trip = db.query(Trip).filter(
        Trip.id == trip_id,
        Trip.user_id == current_user.id
    ).first()
    
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )
    
    db.delete(trip)
    db.commit()
    
    return {"message": "Trip deleted successfully"}