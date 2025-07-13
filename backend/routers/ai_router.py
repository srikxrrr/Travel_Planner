from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import random
import uuid

from ..database import get_db
from ..auth import get_current_user
from ..models import User, AITripPlan, Destination
from ..schemas import AITripPlanRequest, AITripPlanResponse, ItineraryDay, ItineraryActivity, EstimatedCost

router = APIRouter()

@router.post("/generate-trip", response_model=AITripPlanResponse)
async def generate_ai_trip_plan(
    request: AITripPlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate an AI-powered trip plan"""
    
    # Generate unique trip ID
    trip_id = f"ai_trip_{uuid.uuid4().hex[:8]}"
    
    # AI-powered itinerary generation (mock implementation)
    itinerary = generate_smart_itinerary(request)
    
    # Calculate estimated costs based on destination and preferences
    estimated_cost = calculate_trip_cost(request)
    
    # Generate travel tips
    travel_tips = generate_travel_tips(request.destination, request.interests)
    
    # Save AI trip plan to database
    ai_plan = AITripPlan(
        user_id=current_user.id,
        destination=request.destination,
        duration=request.duration,
        travelers=request.travelers,
        budget=request.budget,
        interests=request.interests,
        generated_plan={
            "itinerary": [day.dict() for day in itinerary],
            "estimated_cost": estimated_cost.dict(),
            "travel_tips": travel_tips
        },
        estimated_cost=estimated_cost.dict()
    )
    
    db.add(ai_plan)
    db.commit()
    
    return AITripPlanResponse(
        id=trip_id,
        destination=request.destination,
        duration=request.duration,
        travelers=request.travelers,
        budget=request.budget,
        interests=request.interests,
        itinerary=itinerary,
        estimated_cost=estimated_cost,
        travel_tips=travel_tips,
        best_time_to_visit=get_best_time_to_visit(request.destination)
    )

def generate_smart_itinerary(request: AITripPlanRequest) -> List[ItineraryDay]:
    """Generate intelligent itinerary based on user preferences"""
    
    # Activity pools based on interests
    activity_pools = {
        "culture": [
            {"name": "Visit Historic District", "description": "Explore ancient architecture and cultural landmarks", "duration": "3 hours", "cost": "$25"},
            {"name": "Local Museum Tour", "description": "Discover art, history, and cultural artifacts", "duration": "2 hours", "cost": "$15"},
            {"name": "Traditional Performance", "description": "Experience local music and dance", "duration": "2 hours", "cost": "$40"},
            {"name": "Heritage Walking Tour", "description": "Guided tour through historical neighborhoods", "duration": "3 hours", "cost": "$30"}
        ],
        "food": [
            {"name": "Food Market Tour", "description": "Taste local specialties and street food", "duration": "2 hours", "cost": "$35"},
            {"name": "Cooking Class", "description": "Learn to prepare traditional dishes", "duration": "4 hours", "cost": "$75"},
            {"name": "Fine Dining Experience", "description": "Michelin-starred restaurant reservation", "duration": "3 hours", "cost": "$120"},
            {"name": "Local Food Walking Tour", "description": "Guided culinary adventure", "duration": "3 hours", "cost": "$50"}
        ],
        "adventure": [
            {"name": "Hiking Expedition", "description": "Scenic mountain or nature trail", "duration": "5 hours", "cost": "$40"},
            {"name": "Water Sports", "description": "Kayaking, surfing, or diving", "duration": "4 hours", "cost": "$80"},
            {"name": "Adventure Park", "description": "Zip-lining and obstacle courses", "duration": "3 hours", "cost": "$60"},
            {"name": "Rock Climbing", "description": "Guided climbing experience", "duration": "4 hours", "cost": "$70"}
        ],
        "nature": [
            {"name": "Botanical Garden Visit", "description": "Explore diverse flora and peaceful gardens", "duration": "2 hours", "cost": "$12"},
            {"name": "Wildlife Safari", "description": "Observe local wildlife in natural habitat", "duration": "6 hours", "cost": "$90"},
            {"name": "Scenic Viewpoint", "description": "Panoramic views and photography", "duration": "2 hours", "cost": "Free"},
            {"name": "Nature Reserve Tour", "description": "Guided eco-tour with expert naturalist", "duration": "4 hours", "cost": "$55"}
        ],
        "shopping": [
            {"name": "Local Markets", "description": "Browse handicrafts and souvenirs", "duration": "2 hours", "cost": "$20"},
            {"name": "Shopping District", "description": "Explore boutiques and local brands", "duration": "3 hours", "cost": "$50"},
            {"name": "Artisan Workshops", "description": "Meet local craftspeople and buy unique items", "duration": "2 hours", "cost": "$30"},
            {"name": "Vintage Shopping", "description": "Hunt for unique vintage finds", "duration": "2 hours", "cost": "$25"}
        ]
    }
    
    # Default activities for any destination
    default_activities = [
        {"name": "City Orientation Walk", "description": "Get familiar with the city layout and main attractions", "duration": "2 hours", "cost": "Free"},
        {"name": "Local Transportation Tour", "description": "Learn to navigate public transport", "duration": "1 hour", "cost": "$5"},
        {"name": "Sunset Viewing", "description": "Find the best spot to watch the sunset", "duration": "1 hour", "cost": "Free"},
        {"name": "Local Café Experience", "description": "Relax at a popular local café", "duration": "1 hour", "cost": "$15"}
    ]
    
    itinerary = []
    
    for day in range(1, request.duration + 1):
        # Determine day theme based on interests and day number
        if day == 1:
            day_title = f"Arrival & First Impressions of {request.destination}"
            focus_interests = ["culture"] if "culture" in request.interests else request.interests[:1]
        elif day == request.duration:
            day_title = f"Final Adventures & Departure from {request.destination}"
            focus_interests = request.interests[:2]
        else:
            day_title = f"Exploring {request.destination} - Day {day}"
            focus_interests = request.interests[:2]
        
        # Generate activities for the day
        activities = []
        
        # Morning activity
        morning_activities = []
        for interest in focus_interests:
            if interest.lower() in activity_pools:
                morning_activities.extend(activity_pools[interest.lower()])
        
        if morning_activities:
            morning_activity = random.choice(morning_activities)
            activities.append(ItineraryActivity(
                time="9:00 AM",
                activity=morning_activity["name"],
                description=morning_activity["description"],
                duration=morning_activity["duration"],
                cost=morning_activity["cost"]
            ))
        
        # Lunch
        activities.append(ItineraryActivity(
            time="12:30 PM",
            activity="Local Lunch",
            description="Try authentic local cuisine at a recommended restaurant",
            duration="1 hour",
            cost="$25"
        ))
        
        # Afternoon activity
        afternoon_activities = []
        for interest in focus_interests:
            if interest.lower() in activity_pools:
                afternoon_activities.extend(activity_pools[interest.lower()])
        
        if afternoon_activities:
            afternoon_activity = random.choice([a for a in afternoon_activities if a not in [morning_activity] if 'morning_activity' in locals()])
            activities.append(ItineraryActivity(
                time="2:30 PM",
                activity=afternoon_activity["name"],
                description=afternoon_activity["description"],
                duration=afternoon_activity["duration"],
                cost=afternoon_activity["cost"]
            ))
        
        # Evening activity
        if day == 1:
            activities.append(ItineraryActivity(
                time="6:00 PM",
                activity="Welcome Dinner",
                description="Celebrate your arrival with a special dinner",
                duration="2 hours",
                cost="$45"
            ))
        else:
            evening_activity = random.choice(default_activities)
            activities.append(ItineraryActivity(
                time="6:00 PM",
                activity=evening_activity["name"],
                description=evening_activity["description"],
                duration=evening_activity["duration"],
                cost=evening_activity["cost"]
            ))
        
        itinerary.append(ItineraryDay(
            day=day,
            title=day_title,
            activities=activities
        ))
    
    return itinerary

def calculate_trip_cost(request: AITripPlanRequest) -> EstimatedCost:
    """Calculate estimated trip costs based on destination and preferences"""
    
    # Base costs per day by budget level
    budget_multipliers = {
        "budget": 0.7,
        "moderate": 1.0,
        "luxury": 1.8
    }
    
    # Base costs per day (moderate budget)
    base_accommodation = 100
    base_food = 60
    base_activities = 50
    base_transport = 30
    
    multiplier = budget_multipliers.get(request.budget, 1.0)
    
    # Calculate daily costs
    daily_accommodation = base_accommodation * multiplier
    daily_food = base_food * multiplier
    daily_activities = base_activities * multiplier
    daily_transport = base_transport * multiplier
    
    # Total costs for the trip
    accommodation = daily_accommodation * request.duration
    food = daily_food * request.duration
    activities = daily_activities * request.duration
    transport = daily_transport * request.duration + 200  # Base transport to destination
    
    # Adjust for number of travelers (accommodation might be shared)
    if request.travelers > 1:
        accommodation = accommodation * (1 + (request.travelers - 1) * 0.6)  # Shared rooms
        food = food * request.travelers
        activities = activities * request.travelers
        transport = transport * request.travelers
    
    total = accommodation + food + activities + transport
    
    return EstimatedCost(
        accommodation=round(accommodation, 2),
        food=round(food, 2),
        activities=round(activities, 2),
        transport=round(transport, 2),
        total=round(total, 2)
    )

def generate_travel_tips(destination: str, interests: List[str]) -> List[str]:
    """Generate personalized travel tips"""
    
    base_tips = [
        f"Download offline maps for {destination} before you travel",
        "Keep copies of important documents in separate locations",
        "Learn a few basic phrases in the local language",
        "Check visa requirements and passport validity",
        "Get travel insurance for peace of mind",
        "Notify your bank about your travel dates",
        "Pack comfortable walking shoes",
        "Bring a portable charger for your devices"
    ]
    
    interest_tips = {
        "culture": [
            "Research local customs and etiquette beforehand",
            "Visit museums early in the morning to avoid crowds",
            "Consider hiring a local guide for deeper cultural insights"
        ],
        "food": [
            "Try street food from busy stalls (high turnover = fresh food)",
            "Ask locals for restaurant recommendations",
            "Be adventurous but know your dietary restrictions"
        ],
        "adventure": [
            "Pack appropriate gear for outdoor activities",
            "Check weather conditions before adventure activities",
            "Consider travel insurance that covers adventure sports"
        ],
        "nature": [
            "Bring binoculars for wildlife viewing",
            "Pack insect repellent and sunscreen",
            "Respect local wildlife and follow park rules"
        ],
        "shopping": [
            "Learn basic bargaining phrases",
            "Keep receipts for customs declarations",
            "Leave extra space in your luggage for purchases"
        ]
    }
    
    tips = base_tips.copy()
    
    for interest in interests:
        if interest.lower() in interest_tips:
            tips.extend(interest_tips[interest.lower()])
    
    return random.sample(tips, min(8, len(tips)))

def get_best_time_to_visit(destination: str) -> str:
    """Get the best time to visit a destination"""
    
    # This would typically query a database or external API
    # For now, return generic advice
    seasonal_advice = {
        "paris": "April-June, September-October",
        "tokyo": "March-May, September-November", 
        "bali": "April-October",
        "new york": "April-June, September-November",
        "london": "May-September",
        "rome": "April-June, September-October"
    }
    
    return seasonal_advice.get(destination.lower(), "Check local weather patterns and tourist seasons")

@router.get("/my-plans", response_model=List[dict])
async def get_my_ai_plans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's AI-generated trip plans"""
    plans = db.query(AITripPlan).filter(AITripPlan.user_id == current_user.id).all()
    
    return [
        {
            "id": plan.id,
            "destination": plan.destination,
            "duration": plan.duration,
            "travelers": plan.travelers,
            "budget": plan.budget,
            "interests": plan.interests,
            "estimated_cost": plan.estimated_cost,
            "created_at": plan.created_at
        }
        for plan in plans
    ]