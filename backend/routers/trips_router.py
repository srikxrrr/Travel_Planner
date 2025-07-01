from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import random

from ..database import get_db
from ..auth import get_current_user
from ..models import User, Trip, Destination, TripStatus
from ..schemas import (
    TripCreate, TripResponse, TripUpdate, TripPlanningRequest, 
    TripPlanningResponse, ItineraryDay, DestinationResponse
)

router = APIRouter()

@router.post("/plan", response_model=TripPlanningResponse)
async def plan_trip(
    planning_request: TripPlanningRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a comprehensive travel plan"""
    
    # Generate trip ID
    trip_id = f"TRIP_{random.randint(100000, 999999)}"
    
    # Calculate number of days
    days = (planning_request.end_date - planning_request.start_date).days
    
    # Generate itinerary
    itinerary = []
    current_date = planning_request.start_date
    
    # Sample activities based on interests
    activities_pool = {
        "culture": [
            {"name": "Visit Local Museum", "duration": 2, "cost": 15},
            {"name": "Historical Walking Tour", "duration": 3, "cost": 25},
            {"name": "Cultural Center Visit", "duration": 2, "cost": 10},
            {"name": "Traditional Market Tour", "duration": 2, "cost": 5}
        ],
        "food": [
            {"name": "Food Walking Tour", "duration": 3, "cost": 40},
            {"name": "Cooking Class", "duration": 4, "cost": 60},
            {"name": "Local Restaurant Experience", "duration": 2, "cost": 30},
            {"name": "Street Food Adventure", "duration": 2, "cost": 15}
        ],
        "nature": [
            {"name": "Nature Park Visit", "duration": 4, "cost": 20},
            {"name": "Hiking Trail", "duration": 5, "cost": 0},
            {"name": "Botanical Garden Tour", "duration": 2, "cost": 12},
            {"name": "Wildlife Sanctuary Visit", "duration": 6, "cost": 35}
        ],
        "adventure": [
            {"name": "Adventure Sports", "duration": 4, "cost": 80},
            {"name": "Zip Lining", "duration": 3, "cost": 50},
            {"name": "Rock Climbing", "duration": 4, "cost": 70},
            {"name": "River Rafting", "duration": 6, "cost": 90}
        ],
        "shopping": [
            {"name": "Shopping District Tour", "duration": 3, "cost": 10},
            {"name": "Local Handicrafts Market", "duration": 2, "cost": 5},
            {"name": "Mall Visit", "duration": 3, "cost": 0},
            {"name": "Souvenir Shopping", "duration": 2, "cost": 20}
        ]
    }
    
    for day in range(days):
        day_activities = []
        daily_cost = 0
        
        # Select activities based on interests and pace
        activities_per_day = 2 if planning_request.pace == "Relaxed" else 4 if planning_request.pace == "Packed" else 3
        
        for interest in planning_request.interests[:2]:  # Limit to 2 interests per day
            if interest.lower() in activities_pool:
                activity = random.choice(activities_pool[interest.lower()])
                day_activities.append({
                    "time": "Morning" if len(day_activities) == 0 else "Afternoon",
                    "activity": activity["name"],
                    "duration": f"{activity['duration']} hours",
                    "estimated_cost": activity["cost"],
                    "category": interest
                })
                daily_cost += activity["cost"]
        
        # Add a meal/restaurant recommendation
        day_activities.append({
            "time": "Evening",
            "activity": "Local Restaurant Dinner",
            "duration": "2 hours",
            "estimated_cost": 25,
            "category": "dining"
        })
        daily_cost += 25
        
        itinerary_day = ItineraryDay(
            day_number=day + 1,
            date=current_date,
            activities=day_activities,
            estimated_cost=daily_cost,
            notes=f"Day {day + 1} focused on {', '.join(planning_request.interests[:2])}"
        )
        itinerary.append(itinerary_day)
        current_date += timedelta(days=1)
    
    # Calculate estimated total cost
    estimated_cost = sum(day.estimated_cost for day in itinerary)
    accommodation_cost = days * 100  # $100 per night average
    transport_cost = 200  # Local transport
    total_cost = estimated_cost + accommodation_cost + transport_cost
    
    # Generate trip summary
    trip_summary = {
        "destination": planning_request.destination,
        "duration": f"{days} days",
        "trip_type": planning_request.trip_type,
        "travelers": planning_request.travelers_count,
        "budget_range": f"${total_cost - 200} - ${total_cost + 200}",
        "accommodation": planning_request.accommodation_preference,
        "pace": planning_request.pace,
        "main_interests": planning_request.interests
    }
    
    # Generate travel tips
    travel_tips = [
        f"Best time to visit {planning_request.destination} for your interests",
        "Pack comfortable walking shoes for city exploration",
        "Learn a few basic phrases in the local language",
        "Keep copies of important documents",
        "Check visa requirements and validity",
        "Get travel insurance for peace of mind",
        "Download offline maps and translation apps",
        "Notify your bank about travel dates"
    ]
    
    # Generate booking timeline
    booking_timeline = [
        {
            "task": "Book flights",
            "recommended_time": "8-12 weeks before travel",
            "priority": "High",
            "estimated_savings": "20-30%"
        },
        {
            "task": "Reserve accommodation",
            "recommended_time": "6-8 weeks before travel", 
            "priority": "High",
            "estimated_savings": "15-25%"
        },
        {
            "task": "Purchase travel insurance",
            "recommended_time": "4-6 weeks before travel",
            "priority": "Medium",
            "estimated_savings": "0%"
        },
        {
            "task": "Book activities and tours",
            "recommended_time": "2-4 weeks before travel",
            "priority": "Medium",
            "estimated_savings": "5-15%"
        }
    ]
    
    return TripPlanningResponse(
        trip_id=trip_id,
        trip_summary=trip_summary,
        itinerary=itinerary,
        flight_options=[],  # Will be populated by booking system
        hotel_options=[],   # Will be populated by booking system
        estimated_total_cost=total_cost,
        travel_tips=travel_tips,
        booking_timeline=booking_timeline
    )

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
        itinerary={}
    )
    
    db.add(trip)
    db.commit()
    db.refresh(trip)
    
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
        created_at=trip.created_at,
        updated_at=trip.updated_at
    )

@router.get("/", response_model=List[TripResponse])
async def get_my_trips(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all trips for the current user"""
    trips = db.query(Trip).filter(Trip.user_id == current_user.id).all()
    
    return [
        TripResponse(
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
            created_at=trip.created_at,
            updated_at=trip.updated_at
        )
        for trip in trips
    ]

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
        created_at=trip.created_at,
        updated_at=trip.updated_at
    )

@router.put("/{trip_id}", response_model=TripResponse)
async def update_trip(
    trip_id: int,
    trip_update: TripUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a trip"""
    trip = db.query(Trip).filter(
        Trip.id == trip_id,
        Trip.user_id == current_user.id
    ).first()
    
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )
    
    # Update only provided fields
    update_data = trip_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(trip, field, value)
    
    db.commit()
    db.refresh(trip)
    
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
        created_at=trip.created_at,
        updated_at=trip.updated_at
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