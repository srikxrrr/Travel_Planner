from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import random
import string
import uuid

from ..database import get_db
from ..auth import get_current_user
from ..models import User, Booking, Flight, Hotel, Train, BookingStatus, BookingType
from ..schemas import (
    FlightSearchRequest, FlightOption, FlightBookingRequest, FlightBookingResponse,
    HotelSearchRequest, HotelOption, HotelBookingRequest, HotelBookingResponse,
    TrainSearchRequest, TrainOption, TrainBookingRequest, TrainBookingResponse,
    BookingListResponse, BookingCancellationRequest, BookingCancellationResponse,
    PaymentRequest, PaymentResponse, BookingBase
)

router = APIRouter()

def generate_booking_reference() -> str:
    """Generate a unique booking reference"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def generate_pnr() -> str:
    """Generate a PNR number for train bookings"""
    return ''.join(random.choices(string.digits, k=10))

# Flight Booking Endpoints
@router.post("/flights/search", response_model=List[FlightOption])
async def search_flights(
    search_request: FlightSearchRequest,
    current_user: User = Depends(get_current_user)
):
    """Search for available flights"""
    # Mock flight data - in production, integrate with real airline APIs
    airlines = [
        "Air India", "IndiGo", "SpiceJet", "Vistara", "Go First", "AirAsia India",
        "Emirates", "Qatar Airways", "Lufthansa", "British Airways", "Singapore Airlines"
    ]
    
    aircraft_types = ["Boeing 737", "Airbus A320", "Boeing 777", "Airbus A330", "Boeing 787"]
    
    flights = []
    base_prices = {
        "Economy": 300,
        "Premium Economy": 600,
        "Business": 1200,
        "First": 2500
    }
    
    for i in range(6):
        airline = random.choice(airlines)
        departure_hour = 6 + (i * 3)
        departure_time = datetime.combine(search_request.departure_date, datetime.min.time()) + timedelta(hours=departure_hour)
        duration = random.randint(90, 480)  # 1.5 to 8 hours
        arrival_time = departure_time + timedelta(minutes=duration)
        
        base_price = base_prices.get(search_request.travel_class, 300)
        price_variation = random.uniform(0.8, 1.5)
        final_price = base_price * price_variation * search_request.passengers
        
        stops = random.randint(0, 2)
        layover_airports = []
        if stops > 0:
            layover_airports = random.sample(["DXB", "DOH", "BKK", "SIN", "FRA"], stops)
        
        flight = FlightOption(
            flight_id=f"{airline.replace(' ', '').upper()}{random.randint(100, 999)}",
            airline=airline,
            flight_number=f"{airline[:2].upper()}{random.randint(100, 999)}",
            aircraft_type=random.choice(aircraft_types),
            departure_time=departure_time,
            arrival_time=arrival_time,
            duration_minutes=duration,
            stops=stops,
            layover_airports=layover_airports,
            price=round(final_price, 2),
            currency="USD",
            available_seats=random.randint(5, 50),
            baggage_included=random.choice([True, False]),
            meal_included=search_request.travel_class in ["Business", "First"],
            cancellation_allowed=True,
            change_allowed=True
        )
        flights.append(flight)
    
    return sorted(flights, key=lambda x: x.price)

@router.post("/flights/book", response_model=FlightBookingResponse)
async def book_flight(
    booking_request: FlightBookingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Book a flight"""
    # In production, validate flight availability and process payment
    booking_reference = generate_booking_reference()
    
    # Create booking record
    booking = Booking(
        user_id=current_user.id,
        booking_reference=booking_reference,
        booking_type=BookingType.FLIGHT,
        provider_name="FlightBooking System",
        service_name=f"Flight {booking_request.flight_id}",
        booking_date=datetime.utcnow(),
        passengers_count=len(booking_request.passengers),
        total_amount=1000.0,  # Calculate from flight search
        currency="USD",
        status=BookingStatus.CONFIRMED,
        confirmation_details={
            "flight_id": booking_request.flight_id,
            "passengers": [p.dict() for p in booking_request.passengers],
            "contact_email": booking_request.contact_email,
            "contact_phone": booking_request.contact_phone
        }
    )
    
    db.add(booking)
    db.commit()
    db.refresh(booking)
    
    # Mock flight details for response
    flight_details = FlightOption(
        flight_id=booking_request.flight_id,
        airline="Air India",
        flight_number="AI101",
        aircraft_type="Boeing 737",
        departure_time=datetime.utcnow() + timedelta(days=7),
        arrival_time=datetime.utcnow() + timedelta(days=7, hours=3),
        duration_minutes=180,
        stops=0,
        layover_airports=[],
        price=1000.0,
        currency="USD",
        available_seats=45,
        baggage_included=True,
        meal_included=True,
        cancellation_allowed=True,
        change_allowed=True
    )
    
    return FlightBookingResponse(
        booking_reference=booking_reference,
        status=BookingStatus.CONFIRMED,
        flight_details=flight_details,
        passengers=booking_request.passengers,
        total_cost=booking.total_amount,
        currency=booking.currency,
        payment_status="Completed",
        cancellation_deadline=datetime.utcnow() + timedelta(hours=24),
        check_in_url=f"https://checkin.airline.com/{booking_reference}",
        created_at=booking.created_at
    )

# Hotel Booking Endpoints
@router.post("/hotels/search", response_model=List[HotelOption])
async def search_hotels(
    search_request: HotelSearchRequest,
    current_user: User = Depends(get_current_user)
):
    """Search for available hotels"""
    hotel_chains = ["Marriott", "Hilton", "Hyatt", "Sheraton", "Radisson", "Taj", "ITC", "Oberoi"]
    room_types = ["Standard Room", "Deluxe Room", "Executive Room", "Suite", "Presidential Suite"]
    amenities = ["WiFi", "Pool", "Gym", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]
    
    hotels = []
    nights = (search_request.check_out_date - search_request.check_in_date).days
    
    for i in range(5):
        star_rating = search_request.star_rating or random.randint(3, 5)
        hotel_name = f"{random.choice(hotel_chains)} {search_request.city}"
        
        # Generate room options
        rooms = []
        for j, room_type in enumerate(room_types[:3]):
            base_price = (star_rating * 50) + (j * 30)
            price_per_night = base_price + random.randint(-20, 50)
            total_price = price_per_night * nights
            
            room = RoomOption(
                room_id=f"ROOM_{i}_{j}",
                room_type=room_type,
                room_name=f"{room_type} - {hotel_name}",
                bed_type=random.choice(["Single", "Double", "Queen", "King"]),
                max_occupancy=search_request.guests,
                room_size=f"{random.randint(25, 60)} sqm",
                amenities=random.sample(amenities, 4),
                price_per_night=price_per_night,
                total_price=total_price,
                currency="USD",
                available_rooms=random.randint(1, 10),
                cancellation_policy="Free cancellation up to 24 hours before check-in",
                breakfast_included=random.choice([True, False]),
                wifi_included=True
            )
            rooms.append(room)
        
        hotel = HotelOption(
            hotel_id=f"HOTEL_{i}",
            hotel_name=hotel_name,
            hotel_chain=random.choice(hotel_chains),
            star_rating=star_rating,
            address=f"{random.randint(1, 999)} Hotel Street, {search_request.city}",
            city=search_request.city,
            country="India",
            latitude=random.uniform(20.0, 30.0),
            longitude=random.uniform(70.0, 80.0),
            phone=f"+91-{random.randint(1000000000, 9999999999)}",
            email=f"reservations@{hotel_name.lower().replace(' ', '')}.com",
            description=f"Luxury {star_rating}-star hotel in the heart of {search_request.city}",
            amenities=random.sample(amenities, 6),
            images=[f"https://example.com/hotel{i}/image{j}.jpg" for j in range(1, 6)],
            rating=round(random.uniform(3.5, 4.8), 1),
            review_count=random.randint(100, 2000),
            distance_to_center=round(random.uniform(0.5, 10.0), 1),
            rooms=rooms
        )
        hotels.append(hotel)
    
    return sorted(hotels, key=lambda x: x.rooms[0].price_per_night)

@router.post("/hotels/book", response_model=HotelBookingResponse)
async def book_hotel(
    booking_request: HotelBookingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Book a hotel"""
    booking_reference = generate_booking_reference()
    
    # Create booking record
    booking = Booking(
        user_id=current_user.id,
        booking_reference=booking_reference,
        booking_type=BookingType.HOTEL,
        provider_name="Hotel Booking System",
        service_name=f"Hotel {booking_request.hotel_id}",
        booking_date=datetime.utcnow(),
        passengers_count=len(booking_request.guests),
        total_amount=500.0,  # Calculate from hotel search
        currency="USD",
        status=BookingStatus.CONFIRMED,
        confirmation_details={
            "hotel_id": booking_request.hotel_id,
            "room_id": booking_request.room_id,
            "guests": [g.dict() for g in booking_request.guests],
            "contact_email": booking_request.contact_email,
            "contact_phone": booking_request.contact_phone
        }
    )
    
    db.add(booking)
    db.commit()
    db.refresh(booking)
    
    # Mock hotel and room details for response
    from ..schemas import RoomOption, HotelOption
    room_details = RoomOption(
        room_id=booking_request.room_id,
        room_type="Deluxe Room",
        room_name="Deluxe Room with City View",
        bed_type="King",
        max_occupancy=len(booking_request.guests),
        room_size="35 sqm",
        amenities=["WiFi", "Minibar", "AC", "TV"],
        price_per_night=150.0,
        total_price=500.0,
        currency="USD",
        available_rooms=5,
        cancellation_policy="Free cancellation up to 24 hours",
        breakfast_included=True,
        wifi_included=True
    )
    
    hotel_details = HotelOption(
        hotel_id=booking_request.hotel_id,
        hotel_name="Grand Hotel",
        hotel_chain="Luxury Chain",
        star_rating=4,
        address="123 Hotel Street",
        city="Mumbai",
        country="India",
        latitude=19.0760,
        longitude=72.8777,
        description="Luxury hotel in the heart of the city",
        amenities=["Pool", "Spa", "Gym", "Restaurant"],
        images=["https://example.com/hotel1.jpg"],
        rating=4.5,
        review_count=1500,
        distance_to_center=2.5,
        rooms=[room_details]
    )
    
    return HotelBookingResponse(
        booking_reference=booking_reference,
        status=BookingStatus.CONFIRMED,
        hotel_details=hotel_details,
        room_details=room_details,
        guests=booking_request.guests,
        check_in_date=datetime.utcnow().date() + timedelta(days=7),
        check_out_date=datetime.utcnow().date() + timedelta(days=10),
        nights=3,
        total_cost=booking.total_amount,
        currency=booking.currency,
        payment_status="Completed",
        cancellation_deadline=datetime.utcnow() + timedelta(hours=24),
        created_at=booking.created_at
    )

# Train Booking Endpoints
@router.post("/trains/search", response_model=List[TrainOption])
async def search_trains(
    search_request: TrainSearchRequest,
    current_user: User = Depends(get_current_user)
):
    """Search for available trains"""
    train_names = [
        "Rajdhani Express", "Shatabdi Express", "Duronto Express", 
        "Garib Rath", "Vande Bharat", "Intercity Express", "Mail Express"
    ]
    
    trains = []
    base_prices = {
        "Sleeper": 500,
        "3A": 1000,
        "2A": 1500,
        "1A": 2500
    }
    
    for i in range(5):
        train_name = random.choice(train_names)
        departure_hour = 6 + (i * 4)
        departure_time = datetime.combine(search_request.departure_date, datetime.min.time()) + timedelta(hours=departure_hour)
        duration = random.randint(300, 720)  # 5 to 12 hours
        arrival_time = departure_time + timedelta(minutes=duration)
        
        base_price = base_prices.get(search_request.train_class, 500)
        price_variation = random.uniform(0.9, 1.3)
        final_price = base_price * price_variation * search_request.passengers
        
        train = TrainOption(
            train_id=f"TRAIN_{i}",
            train_name=train_name,
            train_number=f"{random.randint(10000, 99999)}",
            departure_time=departure_time,
            arrival_time=arrival_time,
            duration_minutes=duration,
            distance_km=random.randint(200, 1500),
            stops=random.sample(["Junction A", "Central B", "Station C", "Terminal D"], random.randint(2, 4)),
            train_class=search_request.train_class,
            available_seats=random.randint(10, 100),
            price=round(final_price, 2),
            currency="INR",
            tatkal_available=random.choice([True, False]),
            waiting_list=random.randint(0, 50),
            chart_status="Chart Not Prepared"
        )
        trains.append(train)
    
    return sorted(trains, key=lambda x: x.price)

@router.post("/trains/book", response_model=TrainBookingResponse)
async def book_train(
    booking_request: TrainBookingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Book a train ticket"""
    booking_reference = generate_booking_reference()
    pnr_number = generate_pnr()
    
    # Create booking record
    booking = Booking(
        user_id=current_user.id,
        booking_reference=booking_reference,
        booking_type=BookingType.TRAIN,
        provider_name="Railway Booking System",
        service_name=f"Train {booking_request.train_id}",
        booking_date=datetime.utcnow(),
        passengers_count=len(booking_request.passengers),
        total_amount=2000.0,  # Calculate from train search
        currency="INR",
        status=BookingStatus.CONFIRMED,
        confirmation_details={
            "train_id": booking_request.train_id,
            "pnr_number": pnr_number,
            "passengers": [p.dict() for p in booking_request.passengers],
            "contact_email": booking_request.contact_email,
            "contact_phone": booking_request.contact_phone
        }
    )
    
    db.add(booking)
    db.commit()
    db.refresh(booking)
    
    # Mock train details for response
    train_details = TrainOption(
        train_id=booking_request.train_id,
        train_name="Rajdhani Express",
        train_number="12001",
        departure_time=datetime.utcnow() + timedelta(days=7),
        arrival_time=datetime.utcnow() + timedelta(days=7, hours=8),
        duration_minutes=480,
        distance_km=800,
        stops=["Junction A", "Central B"],
        train_class="3A",
        available_seats=45,
        price=2000.0,
        currency="INR",
        tatkal_available=True,
        waiting_list=5,
        chart_status="Chart Prepared"
    )
    
    # Generate seat assignments
    seat_numbers = [f"A{i+1}" for i in range(len(booking_request.passengers))]
    coach_numbers = ["S1"] * len(booking_request.passengers)
    
    return TrainBookingResponse(
        booking_reference=booking_reference,
        pnr_number=pnr_number,
        status=BookingStatus.CONFIRMED,
        train_details=train_details,
        passengers=booking_request.passengers,
        seat_numbers=seat_numbers,
        coach_numbers=coach_numbers,
        total_cost=booking.total_amount,
        currency=booking.currency,
        booking_status="Confirmed",
        chart_status="Chart Prepared",
        cancellation_charges=200.0,
        created_at=booking.created_at
    )

# General Booking Management
@router.get("/my-bookings", response_model=BookingListResponse)
async def get_my_bookings(
    page: int = 1,
    page_size: int = 10,
    booking_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's bookings"""
    query = db.query(Booking).filter(Booking.user_id == current_user.id)
    
    if booking_type:
        query = query.filter(Booking.booking_type == booking_type)
    
    total_count = query.count()
    bookings = query.offset((page - 1) * page_size).limit(page_size).all()
    
    booking_list = [
        BookingBase(
            booking_type=booking.booking_type,
            booking_reference=booking.booking_reference,
            status=booking.status,
            total_cost=booking.total_amount,
            currency=booking.currency,
            created_at=booking.created_at
        )
        for booking in bookings
    ]
    
    return BookingListResponse(
        bookings=booking_list,
        total_count=total_count,
        page=page,
        page_size=page_size
    )

@router.post("/cancel", response_model=BookingCancellationResponse)
async def cancel_booking(
    cancellation_request: BookingCancellationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel a booking"""
    booking = db.query(Booking).filter(
        Booking.booking_reference == cancellation_request.booking_reference,
        Booking.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if booking.status == BookingStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking is already cancelled"
        )
    
    # Calculate refund amount (mock calculation)
    cancellation_charges = booking.total_amount * 0.1  # 10% cancellation charges
    refund_amount = booking.total_amount - cancellation_charges
    
    # Update booking status
    booking.status = BookingStatus.CANCELLED
    db.commit()
    
    return BookingCancellationResponse(
        booking_reference=booking.booking_reference,
        cancellation_status="Confirmed",
        refund_amount=refund_amount,
        refund_method="Original Payment Method",
        processing_time="3-5 business days",
        cancellation_charges=cancellation_charges
    )

@router.post("/payment", response_model=PaymentResponse)
async def process_payment(
    payment_request: PaymentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Process payment for a booking"""
    booking = db.query(Booking).filter(
        Booking.booking_reference == payment_request.booking_reference,
        Booking.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Mock payment processing
    payment_id = str(uuid.uuid4())
    transaction_id = f"TXN{random.randint(100000, 999999)}"
    
    return PaymentResponse(
        payment_id=payment_id,
        booking_reference=payment_request.booking_reference,
        amount=payment_request.amount,
        currency=payment_request.currency,
        status="Success",
        payment_method=payment_request.payment_method,
        transaction_id=transaction_id,
        created_at=datetime.utcnow()
    )