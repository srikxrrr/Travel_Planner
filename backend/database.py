from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./travel_planner.db"
)

# For SQLite (development)
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
async def init_db():
    from .models import Base
    Base.metadata.create_all(bind=engine)
    
    # Seed initial data
    await seed_destinations()

async def seed_destinations():
    """Seed the database with popular destinations"""
    from sqlalchemy.orm import Session
    from .models import Destination
    
    db = SessionLocal()
    
    # Check if destinations already exist
    if db.query(Destination).count() > 0:
        db.close()
        return
    
    destinations = [
        {
            "name": "Paris",
            "country": "France",
            "city": "Paris",
            "latitude": 48.8566,
            "longitude": 2.3522,
            "description": "The City of Light, famous for its art, fashion, gastronomy, and culture.",
            "best_time_to_visit": "April-June, September-October",
            "average_budget_per_day": 150.0,
            "safety_rating": 8.5,
            "tourist_rating": 9.2,
            "image_url": "https://images.pexels.com/photos/338515/pexels-photo-338515.jpeg?auto=compress&cs=tinysrgb&w=800",
            "attractions": [
                {"name": "Eiffel Tower", "type": "landmark"},
                {"name": "Louvre Museum", "type": "museum"},
                {"name": "Notre-Dame Cathedral", "type": "religious"}
            ],
            "local_cuisine": [
                {"name": "Croissant", "type": "pastry"},
                {"name": "Coq au Vin", "type": "main_dish"},
                {"name": "Macarons", "type": "dessert"}
            ]
        },
        {
            "name": "Tokyo",
            "country": "Japan",
            "city": "Tokyo",
            "latitude": 35.6762,
            "longitude": 139.6503,
            "description": "A vibrant metropolis blending traditional culture with cutting-edge technology.",
            "best_time_to_visit": "March-May, September-November",
            "average_budget_per_day": 200.0,
            "safety_rating": 9.5,
            "tourist_rating": 9.0,
            "image_url": "https://images.pexels.com/photos/2506923/pexels-photo-2506923.jpeg?auto=compress&cs=tinysrgb&w=800",
            "attractions": [
                {"name": "Senso-ji Temple", "type": "religious"},
                {"name": "Tokyo Skytree", "type": "landmark"},
                {"name": "Shibuya Crossing", "type": "landmark"}
            ],
            "local_cuisine": [
                {"name": "Sushi", "type": "main_dish"},
                {"name": "Ramen", "type": "main_dish"},
                {"name": "Tempura", "type": "main_dish"}
            ]
        },
        {
            "name": "Bali",
            "country": "Indonesia",
            "city": "Denpasar",
            "latitude": -8.3405,
            "longitude": 115.0920,
            "description": "Tropical paradise known for its beaches, temples, and vibrant culture.",
            "best_time_to_visit": "April-October",
            "average_budget_per_day": 80.0,
            "safety_rating": 7.5,
            "tourist_rating": 8.8,
            "image_url": "https://images.pexels.com/photos/2474690/pexels-photo-2474690.jpeg?auto=compress&cs=tinysrgb&w=800",
            "attractions": [
                {"name": "Tanah Lot Temple", "type": "religious"},
                {"name": "Ubud Rice Terraces", "type": "nature"},
                {"name": "Mount Batur", "type": "nature"}
            ],
            "local_cuisine": [
                {"name": "Nasi Goreng", "type": "main_dish"},
                {"name": "Satay", "type": "main_dish"},
                {"name": "Gado-gado", "type": "salad"}
            ]
        }
    ]
    
    for dest_data in destinations:
        destination = Destination(**dest_data)
        db.add(destination)
    
    db.commit()
    db.close()