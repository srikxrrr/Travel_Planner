THIS SHOULD BE A LINTER ERRORfrom pydantic import BaseModel, EmailStr, Field, validator
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

# User preferences schemas
class UserPreferencesBase(BaseSchema):
    preferred_budget_min: Optional[float] = None
    preferred_budget_max: Optional[float] = None
    preferred_accommodation_type: Optional[str] = None
    preferred_travel_class: Optional[str] = None
    dietary_restrictions: Optional[List[str]] = []
    travel_interests: Optional[List[str]] = []
    accessibility_needs: Optional[List[str]] = []
    preferred_airlines: Optional[List[str]] = []
    preferred_hotel_chains: Optional[List[str]] = []

class UserPreferencesCreate(UserPreferencesBase):
    pass

class UserPreferencesUpdate(UserPreferencesBase):
    pass

class UserPreferencesResponse(UserPreferencesBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

# Destination schemas
class DestinationBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[str] = None
    currency: Optional[str] = None
    language: Optional[str] = None
    description: Optional[str] = None
    best_time_to_visit: Optional[str] = None
    average_budget_per_day: Optional[float] = None
    safety_rating: Optional[float] = Field(None, ge=0, le=10)
    tourist_rating: Optional[float] = Field(None, ge=0, le=10)

class DestinationCreate(DestinationBase):
    weather_info: Optional[Dict[str, Any]] = {}
    attractions: Optional[List[Dict[str, Any]]] = []
    local_cuisine: Optional[List[Dict[str, Any]]] = []
    transportation_info: Optional[Dict[str, Any]] = {}

class DestinationUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    best_time_to_visit: Optional[str] = None
    average_budget_per_day: Optional[float] = None
    safety_rating: Optional[float] = Field(None, ge=0, le=10)
    tourist_rating: Optional[float] = Field(None, ge=0, le=10)

class DestinationResponse(DestinationBase):
    id: int
    weather_info: Dict[str, Any]
    attractions: List[Dict[str, Any]]
    local_cuisine: List[Dict[str, Any]]
    transportation_info: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None

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

    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v

class TripCreate(TripBase):
    destination_id: int
    interests: Optional[List[str]] = []

class TripUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    total_budget: Optional[float] = None
    travelers_count: Optional[int] = None
    trip_type: Optional[str] = None
    accommodation_preference: Optional[str] = None
    pace: Optional[str] = None
    special_requests: Optional[str] = None
    status: Optional[TripStatusEnum] = None

class TripResponse(TripBase):
    id: int
    user_id: int
    destination_id: int
    spent_amount: float
    interests: List[str]
    status: TripStatusEnum
    itinerary: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None
    destination: Optional[DestinationResponse] = None

# Booking schemas
class BookingBase(BaseSchema):
    booking_type: BookingTypeEnum
    provider_name: Optional[str] = None
    service_name: str = Field(..., min_length=1, max_length=200)
    booking_date: datetime
    service_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    passengers_count: int = Field(1, ge=1, le=20)
    total_amount: float = Field(..., ge=0)
    currency: str = Field("USD", min_length=3, max_length=3)
    special_requests: Optional[str] = None

class BookingCreate(BookingBase):
    trip_id: Optional[int] = None
    confirmation_details: Optional[Dict[str, Any]] = {}
    cancellation_policy: Optional[str] = None

class BookingUpdate(BaseSchema):
    service_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    passengers_count: Optional[int] = None
    total_amount: Optional[float] = None
    status: Optional[BookingStatusEnum] = None
    special_requests: Optional[str] = None

class BookingResponse(BookingBase):
    id: int
    user_id: int
    trip_id: Optional[int] = None
    booking_reference: str
    status: BookingStatusEnum
    confirmation_details: Dict[str, Any]
    cancellation_policy: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

# Flight schemas
class FlightBase(BaseSchema):
    airline: str = Field(..., min_length=1, max_length=100)
    flight_number: str = Field(..., min_length=1, max_length=20)
    origin_airport: str = Field(..., min_length=3, max_length=10)
    destination_airport: str = Field(..., min_length=3, max_length=10)
    departure_time: datetime
    arrival_time: datetime
    aircraft_type: Optional[str] = None
    travel_class: str = Field(..., min_length=1, max_length=50)

class FlightCreate(FlightBase):
    booking_id: int
    duration_minutes: Optional[int] = None
    baggage_allowance: Optional[Dict[str, Any]] = {}
    meal_preference: Optional[str] = None
    seat_numbers: Optional[List[str]] = []
    layovers: Optional[List[Dict[str, Any]]] = []

class FlightResponse(FlightBase):
    id: int
    booking_id: int
    duration_minutes: Optional[int] = None
    baggage_allowance: Dict[str, Any]
    meal_preference: Optional[str] = None
    seat_numbers: List[str]
    layovers: List[Dict[str, Any]]
    created_at: datetime

# Hotel schemas
class HotelBase(BaseSchema):
    hotel_name: str = Field(..., min_length=1, max_length=200)
    hotel_chain: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    star_rating: Optional[float] = Field(None, ge=0, le=5)
    check_in_date: datetime
    check_out_date: datetime
    room_type: Optional[str] = None
    room_count: int = Field(1, ge=1, le=10)
    guest_count: int = Field(1, ge=1, le=20)

class HotelCreate(HotelBase):
    booking_id: int
    amenities: Optional[List[str]] = []
    meal_plan: Optional[str] = None
    cancellation_policy: Optional[str] = None

class HotelResponse(HotelBase):
    id: int
    booking_id: int
    amenities: List[str]
    meal_plan: Optional[str] = None
    cancellation_policy: Optional[str] = None
    created_at: datetime

# Train schemas
class TrainBase(BaseSchema):
    train_name: str = Field(..., min_length=1, max_length=100)
    train_number: str = Field(..., min_length=1, max_length=20)
    origin_station: str = Field(..., min_length=1, max_length=100)
    destination_station: str = Field(..., min_length=1, max_length=100)
    departure_time: datetime
    arrival_time: datetime
    train_class: str = Field(..., min_length=1, max_length=50)

class TrainCreate(TrainBase):
    booking_id: int
    duration_minutes: Optional[int] = None
    seat_numbers: Optional[List[str]] = []
    berth_preferences: Optional[Dict[str, Any]] = {}
    meal_preference: Optional[str] = None

class TrainResponse(TrainBase):
    id: int
    booking_id: int
    duration_minutes: Optional[int] = None
    seat_numbers: List[str]
    berth_preferences: Dict[str, Any]
    meal_preference: Optional[str] = None
    created_at: datetime

# Search schemas
class FlightSearchRequest(BaseSchema):
    origin: str = Field(..., min_length=3, max_length=3)
    destination: str = Field(..., min_length=3, max_length=3)
    departure_date: date
    return_date: Optional[date] = None
    passengers: int = Field(1, ge=1, le=9)
    travel_class: str = "Economy"

class TrainSearchRequest(BaseSchema):
    origin: str = Field(..., min_length=1, max_length=100)
    destination: str = Field(..., min_length=1, max_length=100)
    departure_date: date
    passengers: int = Field(1, ge=1, le=6)
    train_class: str = "Sleeper"

class HotelSearchRequest(BaseSchema):
    city: str = Field(..., min_length=1, max_length=100)
    check_in_date: date
    check_out_date: date
    guests: int = Field(1, ge=1, le=10)
    rooms: int = Field(1, ge=1, le=5)
    star_rating: Optional[int] = Field(None, ge=1, le=5)

# Recommendation schemas
class RecommendationBase(BaseSchema):
    category: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=10)
    price_range: Optional[str] = None
    location: Optional[str] = None

class RecommendationCreate(RecommendationBase):
    destination_id: int
    opening_hours: Optional[Dict[str, str]] = {}
    contact_info: Optional[Dict[str, str]] = {}
    tags: Optional[List[str]] = []
    image_urls: Optional[List[str]] = []
    external_links: Optional[Dict[str, str]] = {}

class RecommendationResponse(RecommendationBase):
    id: int
    destination_id: int
    opening_hours: Dict[str, str]
    contact_info: Dict[str, str]
    tags: List[str]
    image_urls: List[str]
    external_links: Dict[str, str]
    created_at: datetime
    updated_at: Optional[datetime] = None

# Weather schemas
class WeatherResponse(BaseSchema):
    destination_id: int
    date: datetime
    temperature_min: Optional[float] = None
    temperature_max: Optional[float] = None
    humidity: Optional[float] = None
    precipitation: Optional[float] = None
    wind_speed: Optional[float] = None
    weather_condition: Optional[str] = None
    weather_description: Optional[str] = None
    uv_index: Optional[float] = None
    visibility: Optional[float] = None

# Trip planning schemas
class TripPlanningRequest(BaseSchema):
    destination: str = Field(..., min_length=1, max_length=100)
    start_date: date
    end_date: date
    budget: Optional[float] = None
    travelers_count: int = Field(1, ge=1, le=20)
    trip_type: str = "Solo"
    accommodation_preference: str = "Hotel"
    interests: List[str] = []
    pace: str = "Balanced"
    special_requests: Optional[str] = None

class ItineraryDay(BaseSchema):
    day_number: int
    date: date
    morning: List[Dict[str, Any]] = []
    afternoon: List[Dict[str, Any]] = []
    evening: List[Dict[str, Any]] = []
    estimated_cost: Optional[float] = None
    notes: Optional[str] = None

class TripPlanningResponse(BaseSchema):
    trip_summary: Dict[str, Any]
    itinerary: List[ItineraryDay]
    recommendations: Dict[str, List[RecommendationResponse]]
    estimated_total_cost: Optional[float] = None
    weather_forecast: List[WeatherResponse] = []
    travel_tips: List[str] = []