from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum as PyEnum
import uuid

Base = declarative_base()

class TripStatus(PyEnum):
    PLANNING = "planning"
    BOOKED = "booked"
    CONFIRMED = "confirmed"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class BookingStatus(PyEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class BookingType(PyEnum):
    FLIGHT = "flight"
    HOTEL = "hotel"
    TRAIN = "train"
    CAR_RENTAL = "car_rental"
    ACTIVITY = "activity"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    phone_number = Column(String(20))
    date_of_birth = Column(DateTime)
    country = Column(String(50))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    trips = relationship("Trip", back_populates="user", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")
    preferences = relationship("UserPreferences", back_populates="user", uselist=False, cascade="all, delete-orphan")

class UserPreferences(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    preferred_budget_min = Column(Float)
    preferred_budget_max = Column(Float)
    preferred_accommodation_type = Column(String(50))
    preferred_travel_class = Column(String(50))
    dietary_restrictions = Column(JSON)
    travel_interests = Column(JSON)
    accessibility_needs = Column(JSON)
    preferred_airlines = Column(JSON)
    preferred_hotel_chains = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="preferences")

class Destination(Base):
    __tablename__ = "destinations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    country = Column(String(100), nullable=False)
    city = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    timezone = Column(String(50))
    currency = Column(String(10))
    language = Column(String(50))
    description = Column(Text)
    best_time_to_visit = Column(String(100))
    average_budget_per_day = Column(Float)
    safety_rating = Column(Float)
    tourist_rating = Column(Float)
    weather_info = Column(JSON)
    attractions = Column(JSON)
    local_cuisine = Column(JSON)
    transportation_info = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    trips = relationship("Trip", back_populates="destination")

class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    total_budget = Column(Float)
    spent_amount = Column(Float, default=0)
    travelers_count = Column(Integer, default=1)
    trip_type = Column(String(50))  # solo, couple, family, group, business
    accommodation_preference = Column(String(50))
    interests = Column(JSON)
    pace = Column(String(50))  # relaxed, balanced, packed
    special_requests = Column(Text)
    status = Column(Enum(TripStatus), default=TripStatus.PLANNING)
    itinerary = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="trips")
    destination = relationship("Destination", back_populates="trips")
    bookings = relationship("Booking", back_populates="trip", cascade="all, delete-orphan")

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    booking_reference = Column(String(20), unique=True, nullable=False)
    booking_type = Column(Enum(BookingType), nullable=False)
    provider_name = Column(String(100))
    service_name = Column(String(200))
    booking_date = Column(DateTime, nullable=False)
    service_date = Column(DateTime)
    end_date = Column(DateTime)
    passengers_count = Column(Integer, default=1)
    total_amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    confirmation_details = Column(JSON)
    cancellation_policy = Column(Text)
    special_requests = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="bookings")
    trip = relationship("Trip", back_populates="bookings")

class Flight(Base):
    __tablename__ = "flights"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    airline = Column(String(100), nullable=False)
    flight_number = Column(String(20), nullable=False)
    origin_airport = Column(String(10), nullable=False)
    destination_airport = Column(String(10), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer)
    aircraft_type = Column(String(50))
    travel_class = Column(String(50))
    baggage_allowance = Column(JSON)
    meal_preference = Column(String(50))
    seat_numbers = Column(JSON)
    layovers = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    booking = relationship("Booking")

class Hotel(Base):
    __tablename__ = "hotels"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    hotel_name = Column(String(200), nullable=False)
    hotel_chain = Column(String(100))
    address = Column(String(500))
    city = Column(String(100))
    country = Column(String(100))
    star_rating = Column(Float)
    check_in_date = Column(DateTime, nullable=False)
    check_out_date = Column(DateTime, nullable=False)
    room_type = Column(String(100))
    room_count = Column(Integer, default=1)
    guest_count = Column(Integer, default=1)
    amenities = Column(JSON)
    meal_plan = Column(String(50))
    cancellation_policy = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    booking = relationship("Booking")

class Train(Base):
    __tablename__ = "trains"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    train_name = Column(String(100), nullable=False)
    train_number = Column(String(20), nullable=False)
    origin_station = Column(String(100), nullable=False)
    destination_station = Column(String(100), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer)
    train_class = Column(String(50))
    seat_numbers = Column(JSON)
    berth_preferences = Column(JSON)
    meal_preference = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    booking = relationship("Booking")

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    category = Column(String(50), nullable=False)  # restaurant, activity, attraction, etc.
    name = Column(String(200), nullable=False)
    description = Column(Text)
    rating = Column(Float)
    price_range = Column(String(50))
    location = Column(String(200))
    opening_hours = Column(JSON)
    contact_info = Column(JSON)
    tags = Column(JSON)
    image_urls = Column(JSON)
    external_links = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    destination = relationship("Destination")

class WeatherData(Base):
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    temperature_min = Column(Float)
    temperature_max = Column(Float)
    humidity = Column(Float)
    precipitation = Column(Float)
    wind_speed = Column(Float)
    weather_condition = Column(String(100))
    weather_description = Column(String(200))
    uv_index = Column(Float)
    visibility = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    destination = relationship("Destination")