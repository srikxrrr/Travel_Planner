from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum

# Enum schemas
class TripStatusEnum(str, Enum):
    PLANNING = "planning"
    BOOKED = "booked"
    CONFIRMED = "confirmed"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class BookingStatusEnum(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class BookingTypeEnum(str, Enum):
    FLIGHT = "flight"
    HOTEL = "hotel"
    TRAIN = "train"
    CAR_RENTAL = "car_rental"
    ACTIVITY = "activity"

# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseSchema):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    country: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseSchema):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    country: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

class UserLogin(BaseSchema):
    username: str
    password: str

class Token(BaseSchema):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

# AI Trip Planning schemas
class AITripPlanRequest(BaseSchema):
    destination: str = Field(..., min_length=1, max_length=200)
    duration: int = Field(..., ge=1, le=30)
    travelers: int = Field(..., ge=1, le=20)
    budget: str = Field(..., description="budget, moderate, luxury")
    interests: List[str] = []

class ItineraryActivity(BaseSchema):
    time: str
    activity: str
    description: str
    cost: Optional[str] = None
    location: Optional[str] = None
    duration: Optional[str] = None

class ItineraryDay(BaseSchema):
    day: int
    title: str
    activities: List[ItineraryActivity]

class EstimatedCost(BaseSchema):
    accommodation: float
    food: float
    activities: float
    transport: float
    total: float

class AITripPlanResponse(BaseSchema):
    id: str
    destination: str
    duration: int
    travelers: int
    budget: str
    interests: List[str]
    itinerary: List[ItineraryDay]
    estimated_cost: EstimatedCost
    travel_tips: List[str] = []
    best_time_to_visit: Optional[str] = None

# Destination schemas
class DestinationBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    best_time_to_visit: Optional[str] = None
    average_budget_per_day: Optional[float] = None
    safety_rating: Optional[float] = Field(None, ge=0, le=10)
    tourist_rating: Optional[float] = Field(None, ge=0, le=10)
    image_url: Optional[str] = None

class DestinationResponse(DestinationBase):
    id: int
    weather_info: Dict[str, Any] = {}
    attractions: List[Dict[str, Any]] = []
    local_cuisine: List[Dict[str, Any]] = []
    created_at: datetime

# Trip schemas
class TripBase(BaseSchema):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    total_budget: Optional[float] = None
    travelers_count: int = Field(1, ge=1, le=20)
    trip_type: Optional[str] = None
    accommodation_preference: Optional[str] = None
    pace: Optional[str] = None
    special_requests: Optional[str] = None

class TripCreate(TripBase):
    destination_id: int
    interests: Optional[List[str]] = []

class TripResponse(TripBase):
    id: int
    user_id: int
    destination_id: int
    spent_amount: float
    interests: List[str]
    status: TripStatusEnum
    itinerary: Dict[str, Any]
    ai_generated: bool
    created_at: datetime
    destination: Optional[DestinationResponse] = None

# Weather schemas
class WeatherResponse(BaseSchema):
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    description: str
    icon: str
    wind_speed: float
    visibility: int

# Recommendation schemas
class RecommendationResponse(BaseSchema):
    id: int
    category: str
    name: str
    description: str
    rating: Optional[float] = None
    price_range: Optional[str] = None
    location: str
    tags: List[str]
    image_urls: List[str] = []

# Search schemas
class DestinationSearchRequest(BaseSchema):
    query: str = Field(..., min_length=1, max_length=200)
    limit: int = Field(10, ge=1, le=50)

class DestinationSearchResponse(BaseSchema):
    name: str
    country: str
    city: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    average_budget: Optional[float] = None
    best_time_to_visit: Optional[str] = None