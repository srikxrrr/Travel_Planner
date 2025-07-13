from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import random
import string

from ..database import get_db
from ..auth import get_current_user
from ..models import User, Booking, BookingStatus, BookingType

router = APIRouter()

def generate_booking_reference() -> str:
    """Generate a unique booking reference"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@router.get("/my-bookings")
async def get_my_bookings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's bookings"""
    bookings = db.query(Booking).filter(Booking.user_id == current_user.id).all()
    
    return [
        {
            "id": booking.id,
            "booking_reference": booking.booking_reference,
            "booking_type": booking.booking_type,
            "service_name": booking.service_name,
            "total_amount": booking.total_amount,
            "currency": booking.currency,
            "status": booking.status,
            "created_at": booking.created_at
        }
        for booking in bookings
    ]

@router.post("/simulate-booking")
async def simulate_booking(
    booking_type: str,
    service_name: str,
    amount: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Simulate a booking for demo purposes"""
    
    booking_reference = generate_booking_reference()
    
    booking = Booking(
        user_id=current_user.id,
        booking_reference=booking_reference,
        booking_type=BookingType(booking_type),
        service_name=service_name,
        total_amount=amount,
        currency="USD",
        status=BookingStatus.CONFIRMED,
        confirmation_details={"simulated": True}
    )
    
    db.add(booking)
    db.commit()
    
    return {
        "booking_reference": booking_reference,
        "status": "confirmed",
        "message": "Booking simulation successful"
    }