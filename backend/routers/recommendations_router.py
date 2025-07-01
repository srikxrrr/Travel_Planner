from fastapi import APIRouter, Depends
from typing import List

from ..auth import get_current_user
from ..models import User
from ..schemas import RecommendationResponse

router = APIRouter()

@router.get("/", response_model=List[RecommendationResponse])
async def get_recommendations(
    destination_id: int = None,
    category: str = None,
    current_user: User = Depends(get_current_user)
):
    """Get travel recommendations"""
    # Mock recommendations
    recommendations = [
        {
            "id": 1,
            "category": "restaurant",
            "name": "Local Cuisine Restaurant",
            "description": "Authentic local dishes in cozy atmosphere",
            "rating": 4.5,
            "price_range": "$$",
            "location": "City Center",
            "tags": ["authentic", "local", "popular"],
            "booking_available": True,
            "booking_url": "https://example.com/book"
        },
        {
            "id": 2,
            "category": "attraction",
            "name": "Historical Museum",
            "description": "Rich collection of local history and artifacts",
            "rating": 4.2,
            "price_range": "$",
            "location": "Old Town",
            "tags": ["history", "culture", "educational"],
            "booking_available": False
        }
    ]
    
    return [RecommendationResponse(**rec) for rec in recommendations]