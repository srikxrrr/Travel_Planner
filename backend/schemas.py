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
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    description: str
    icon: str
    wind_speed: float
    wind_direction: int
    visibility: int
    uv_index: Optional[float] = None

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
    activities: List[Dict[str, Any]] = []
    estimated_cost: Optional[float] = None
    weather: Optional[WeatherResponse] = None
    notes: Optional[str] = None

class TripPlanningResponse(BaseSchema):
    trip_summary: Dict[str, Any]
    itinerary: List[ItineraryDay]
    destination_info: Dict[str, Any]
    estimated_total_cost: Optional[float] = None
    travel_tips: List[str] = []

# Open source API integration schemas
class OpenStreetMapLocation(BaseSchema):
    display_name: str
    latitude: float
    longitude: float
    country: str
    city: Optional[str] = None
    state: Optional[str] = None
    address: Dict[str, Any]

class WikipediaInfo(BaseSchema):
    title: str
    extract: str
    url: str
    thumbnail: Optional[str] = None

# Search schemas for open APIs
class LocationSearchRequest(BaseSchema):
    query: str = Field(..., min_length=1, max_length=200)
    limit: int = Field(5, ge=1, le=20)

class POISearchRequest(BaseSchema):
    location: str
    category: Optional[str] = None  # tourism, food, accommodation, etc.
    radius: int = Field(5000, ge=100, le=50000)  # in meters

class POIResponse(BaseSchema):
    name: str
    category: str
    latitude: float
    longitude: float
    address: Optional[str] = None
    rating: Optional[float] = None
    tags: Dict[str, str]
    distance: Optional[float] = None

# Booking simulation schemas (for demo purposes)
class FlightSearchRequest(BaseSchema):
    origin: str = Field(..., min_length=3, max_length=3)
    destination: str = Field(..., min_length=3, max_length=3)
    departure_date: date
    return_date: Optional[date] = None
    passengers: int = Field(1, ge=1, le=9)
    travel_class: str = "Economy"

class TrainSearchRequest(BaseSchema):
    origin: str
    destination: str
    departure_date: date
    passengers: int = Field(1, ge=1, le=6)
    train_class: str = "Sleeper"

class HotelSearchRequest(BaseSchema):
    city: str
    check_in_date: date
    check_out_date: date
    guests: int = Field(1, ge=1, le=10)
    rooms: int = Field(1, ge=1, le=5)

class BookingResponse(BaseSchema):
    booking_id: str
    type: BookingTypeEnum
    provider: str
    service_name: str
    total_cost: float
    currency: str
    status: BookingStatusEnum
    confirmation_details: Dict[str, Any]

# Flight Booking Schemas
class FlightSearchRequest(BaseSchema):
    origin: str = Field(..., min_length=3, max_length=3, description="Origin airport code (IATA)")
    destination: str = Field(..., min_length=3, max_length=3, description="Destination airport code (IATA)")
    departure_date: date
    return_date: Optional[date] = None
    passengers: int = Field(1, ge=1, le=9)
    travel_class: str = Field("Economy", description="Economy, Premium Economy, Business, First")

class PassengerInfo(BaseSchema):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    date_of_birth: date
    gender: str = Field(..., description="Male, Female, Other")
    passport_number: Optional[str] = None
    nationality: str = Field(..., min_length=2, max_length=3)
    meal_preference: Optional[str] = None
    special_assistance: Optional[str] = None

class FlightOption(BaseSchema):
    flight_id: str
    airline: str
    flight_number: str
    aircraft_type: str
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    stops: int
    layover_airports: List[str] = []
    price: float
    currency: str = "USD"
    available_seats: int
    baggage_included: bool
    meal_included: bool
    cancellation_allowed: bool
    change_allowed: bool

class FlightBookingRequest(BaseSchema):
    flight_id: str
    passengers: List[PassengerInfo]
    contact_email: EmailStr
    contact_phone: str
    emergency_contact: Dict[str, str]
    seat_preferences: Optional[List[str]] = []
    special_requests: Optional[str] = None

class FlightBookingResponse(BaseSchema):
    booking_reference: str
    status: BookingStatusEnum
    flight_details: FlightOption
    passengers: List[PassengerInfo]
    total_cost: float
    currency: str
    payment_status: str
    cancellation_deadline: Optional[datetime] = None
    check_in_url: Optional[str] = None
    created_at: datetime

# Hotel Booking Schemas
class HotelSearchRequest(BaseSchema):
    city: str = Field(..., min_length=1, max_length=100)
    check_in_date: date
    check_out_date: date
    guests: int = Field(1, ge=1, le=10)
    rooms: int = Field(1, ge=1, le=5)
    star_rating: Optional[int] = Field(None, ge=1, le=5)
    max_price_per_night: Optional[float] = None
    amenities: Optional[List[str]] = []

    @validator('check_out_date')
    def check_out_after_check_in(cls, v, values):
        if 'check_in_date' in values and v <= values['check_in_date']:
            raise ValueError('Check-out date must be after check-in date')
        return v

class RoomOption(BaseSchema):
    room_id: str
    room_type: str
    room_name: str
    bed_type: str
    max_occupancy: int
    room_size: Optional[str] = None
    amenities: List[str] = []
    price_per_night: float
    total_price: float
    currency: str = "USD"
    available_rooms: int
    cancellation_policy: str
    breakfast_included: bool
    wifi_included: bool

class HotelOption(BaseSchema):
    hotel_id: str
    hotel_name: str
    hotel_chain: Optional[str] = None
    star_rating: int
    address: str
    city: str
    country: str
    latitude: float
    longitude: float
    phone: Optional[str] = None
    email: Optional[str] = None
    description: str
    amenities: List[str] = []
    images: List[str] = []
    rating: float
    review_count: int
    distance_to_center: float
    rooms: List[RoomOption]

class GuestInfo(BaseSchema):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    nationality: Optional[str] = None
    passport_number: Optional[str] = None

class HotelBookingRequest(BaseSchema):
    hotel_id: str
    room_id: str
    guests: List[GuestInfo]
    contact_email: EmailStr
    contact_phone: str
    special_requests: Optional[str] = None
    arrival_time: Optional[str] = None
    smoking_preference: bool = False

class HotelBookingResponse(BaseSchema):
    booking_reference: str
    status: BookingStatusEnum
    hotel_details: HotelOption
    room_details: RoomOption
    guests: List[GuestInfo]
    check_in_date: date
    check_out_date: date
    nights: int
    total_cost: float
    currency: str
    payment_status: str
    cancellation_deadline: Optional[datetime] = None
    created_at: datetime

# Train Booking Schemas
class TrainSearchRequest(BaseSchema):
    origin_station: str = Field(..., min_length=1, max_length=100)
    destination_station: str = Field(..., min_length=1, max_length=100)
    departure_date: date
    passengers: int = Field(1, ge=1, le=6)
    train_class: str = Field("Sleeper", description="Sleeper, 3A, 2A, 1A")
    quota: Optional[str] = Field("GN", description="General, Ladies, Senior Citizen, etc.")

class TrainOption(BaseSchema):
    train_id: str
    train_name: str
    train_number: str
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    distance_km: int
    stops: List[str] = []
    train_class: str
    available_seats: int
    price: float
    currency: str = "INR"
    tatkal_available: bool
    waiting_list: int
    chart_status: str

class TrainPassengerInfo(BaseSchema):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., ge=1, le=120)
    gender: str = Field(..., description="Male, Female, Transgender")
    berth_preference: Optional[str] = Field(None, description="Lower, Middle, Upper, Side Lower, Side Upper")
    food_choice: Optional[str] = Field(None, description="Veg, Non-Veg")

class TrainBookingRequest(BaseSchema):
    train_id: str
    passengers: List[TrainPassengerInfo]
    contact_email: EmailStr
    contact_phone: str
    id_proof_type: str = Field(..., description="Aadhar, PAN, Passport, etc.")
    id_proof_number: str
    auto_upgrade: bool = False

class TrainBookingResponse(BaseSchema):
    booking_reference: str
    pnr_number: str
    status: BookingStatusEnum
    train_details: TrainOption
    passengers: List[TrainPassengerInfo]
    seat_numbers: List[str] = []
    coach_numbers: List[str] = []
    total_cost: float
    currency: str
    booking_status: str  # Confirmed, RAC, Waiting List
    chart_status: str
    cancellation_charges: float
    created_at: datetime

# Generic Booking Management
class BookingBase(BaseSchema):
    booking_type: BookingTypeEnum
    booking_reference: str
    status: BookingStatusEnum
    total_cost: float
    currency: str
    created_at: datetime

class BookingListResponse(BaseSchema):
    bookings: List[BookingBase]
    total_count: int
    page: int
    page_size: int

class BookingCancellationRequest(BaseSchema):
    booking_reference: str
    cancellation_reason: str
    refund_to_original_method: bool = True

class BookingCancellationResponse(BaseSchema):
    booking_reference: str
    cancellation_status: str
    refund_amount: float
    refund_method: str
    processing_time: str
    cancellation_charges: float

# Payment Schemas
class PaymentRequest(BaseSchema):
    booking_reference: str
    payment_method: str = Field(..., description="Credit Card, Debit Card, UPI, Net Banking, Wallet")
    amount: float
    currency: str = "USD"
    card_details: Optional[Dict[str, str]] = None
    billing_address: Optional[Dict[str, str]] = None

class PaymentResponse(BaseSchema):
    payment_id: str
    booking_reference: str
    amount: float
    currency: str
    status: str
    payment_method: str
    transaction_id: str
    created_at: datetime

# Trip Planning with Bookings
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
    include_flights: bool = True
    include_hotels: bool = True
    include_activities: bool = True

class ItineraryDay(BaseSchema):
    day_number: int
    date: date
    activities: List[Dict[str, Any]] = []
    estimated_cost: Optional[float] = None
    notes: Optional[str] = None

class TripPlanningResponse(BaseSchema):
    trip_id: str
    trip_summary: Dict[str, Any]
    itinerary: List[ItineraryDay]
    flight_options: List[FlightOption] = []
    hotel_options: List[HotelOption] = []
    estimated_total_cost: Optional[float] = None
    travel_tips: List[str] = []
    booking_timeline: List[Dict[str, Any]] = []

# Search and Discovery
class LocationSearchRequest(BaseSchema):
    query: str = Field(..., min_length=1, max_length=200)
    limit: int = Field(5, ge=1, le=20)

class LocationResponse(BaseSchema):
    name: str
    country: str
    city: Optional[str] = None
    latitude: float
    longitude: float
    description: Optional[str] = None
    best_time_to_visit: Optional[str] = None
    average_budget: Optional[float] = None

class RecommendationResponse(BaseSchema):
    id: int
    category: str
    name: str
    description: str
    rating: Optional[float] = None
    price_range: Optional[str] = None
    location: str
    tags: List[str]
    booking_available: bool = False
    booking_url: Optional[str] = None

# Destination and Weather
class WeatherResponse(BaseSchema):
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    description: str
    icon: str
    wind_speed: float
    visibility: int

class DestinationResponse(BaseSchema):
    id: int
    name: str
    country: str
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    weather_info: Optional[WeatherResponse] = None
    attractions: List[Dict[str, Any]] = []
    local_cuisine: List[Dict[str, Any]] = []
    created_at: datetime