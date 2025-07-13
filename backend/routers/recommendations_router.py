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
    # Mock recommendations - in production, this would query the database
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
            "image_urls": ["https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg"]
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
            "image_urls": ["https://images.pexels.com/photos/1004584/pexels-photo-1004584.jpeg"]
        },
        {
            "id": 3,
            "category": "activity",
            "name": "Guided Walking Tour",
            "description": "Explore hidden gems with local expert guide",
            "rating": 4.8,
            "price_range": "$$",
            "location": "Various",
            "tags": ["walking", "guide", "hidden gems"],
            "image_urls": ["https://images.pexels.com/photos/1320684/pexels-photo-1320684.jpeg"]
        }
    ]
    
    # Filter by category if provided
    if category:
        recommendations = [r for r in recommendations if r["category"] == category]
    
    return [RecommendationResponse(**rec) for rec in recommendations]