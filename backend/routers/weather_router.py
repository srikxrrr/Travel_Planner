from fastapi import APIRouter, Depends
from typing import List
import random

from ..auth import get_current_user
from ..models import User
from ..schemas import WeatherResponse

router = APIRouter()

@router.get("/current", response_model=WeatherResponse)
async def get_current_weather(
    city: str,
    current_user: User = Depends(get_current_user)
):
    """Get current weather for a city"""
    # Mock weather data - in production, integrate with OpenWeatherMap API
    weather_conditions = ["Clear", "Cloudy", "Rainy", "Sunny", "Partly Cloudy"]
    icons = ["01d", "02d", "10d", "01d", "03d"]
    
    condition = random.choice(weather_conditions)
    icon = random.choice(icons)
    
    return WeatherResponse(
        temperature=random.uniform(15, 35),
        feels_like=random.uniform(15, 35),
        humidity=random.randint(30, 90),
        pressure=random.randint(1000, 1020),
        description=condition,
        icon=icon,
        wind_speed=random.uniform(0, 15),
        visibility=random.randint(5, 15)
    )

@router.get("/forecast", response_model=List[WeatherResponse])
async def get_weather_forecast(
    city: str,
    days: int = 5,
    current_user: User = Depends(get_current_user)
):
    """Get weather forecast for a city"""
    forecast = []
    for _ in range(days):
        weather_conditions = ["Clear", "Cloudy", "Rainy", "Sunny", "Partly Cloudy"]
        icons = ["01d", "02d", "10d", "01d", "03d"]
        
        condition = random.choice(weather_conditions)
        icon = random.choice(icons)
        
        forecast.append(WeatherResponse(
            temperature=random.uniform(15, 35),
            feels_like=random.uniform(15, 35),
            humidity=random.randint(30, 90),
            pressure=random.randint(1000, 1020),
            description=condition,
            icon=icon,
            wind_speed=random.uniform(0, 15),
            visibility=random.randint(5, 15)
        ))
    
    return forecast