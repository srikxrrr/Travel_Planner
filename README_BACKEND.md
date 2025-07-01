# Travel Planner Backend API

A comprehensive travel planning and booking backend API built with FastAPI, featuring flight/hotel/train booking, trip planning, user management, and more.

## Features

### 🔐 Authentication & User Management
- JWT-based authentication
- User registration and login
- Profile management
- Secure password hashing

### ✈️ Booking Systems
- **Flight Booking**: Search, compare, and book flights
- **Hotel Booking**: Find and reserve accommodations
- **Train Booking**: Book train tickets with seat selection
- Payment processing simulation
- Booking management and cancellation

### 🗺️ Trip Planning
- AI-powered itinerary generation
- Personalized recommendations based on interests
- Budget estimation and tracking
- Multi-day trip planning
- Activity suggestions by category

### 🌍 Destination Management
- Destination search and discovery
- Popular destinations listing
- Detailed destination information
- Weather forecasts and conditions

### 📊 Additional Features
- Travel recommendations
- Weather integration
- Booking history and management
- Trip status tracking
- Cost estimation and budget planning

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLAlchemy with PostgreSQL/SQLite
- **Authentication**: JWT with PassLib
- **Documentation**: Auto-generated OpenAPI/Swagger
- **Validation**: Pydantic models
- **Testing**: Pytest

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user info
- `PUT /api/v1/auth/me` - Update user profile

### Trip Planning
- `POST /api/v1/trips/plan` - Generate trip plan
- `POST /api/v1/trips/` - Create trip
- `GET /api/v1/trips/` - Get user trips
- `GET /api/v1/trips/{id}` - Get trip details
- `PUT /api/v1/trips/{id}` - Update trip
- `DELETE /api/v1/trips/{id}` - Delete trip

### Bookings
- `POST /api/v1/bookings/flights/search` - Search flights
- `POST /api/v1/bookings/flights/book` - Book flight
- `POST /api/v1/bookings/hotels/search` - Search hotels
- `POST /api/v1/bookings/hotels/book` - Book hotel
- `POST /api/v1/bookings/trains/search` - Search trains
- `POST /api/v1/bookings/trains/book` - Book train
- `GET /api/v1/bookings/my-bookings` - Get user bookings
- `POST /api/v1/bookings/cancel` - Cancel booking
- `POST /api/v1/bookings/payment` - Process payment

### Destinations & Weather
- `GET /api/v1/destinations/search` - Search destinations
- `GET /api/v1/destinations/popular` - Popular destinations
- `GET /api/v1/weather/current` - Current weather
- `GET /api/v1/weather/forecast` - Weather forecast

## Installation & Setup

### Prerequisites
- Python 3.9+
- pip or poetry
- PostgreSQL (optional, SQLite for development)

### Quick Start

1. **Clone and Setup**
```bash
cd backend
pip install -r requirements.txt
```

2. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Database Setup**
```bash
# The database will be automatically created on first run
# For PostgreSQL, create the database first:
# createdb travel_planner
```

4. **Run the Application**
```bash
# Development server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or using the main file
python backend/main.py
```

5. **Access the API**
- API Documentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc
- Health Check: http://localhost:8000/api/v1/health

## Usage Examples

### 1. User Registration and Authentication

```bash
# Register a new user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "traveler123",
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "secure_password123"
  }'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "traveler123",
    "password": "secure_password123"
  }'
```

### 2. Trip Planning

```bash
# Generate a trip plan
curl -X POST "http://localhost:8000/api/v1/trips/plan" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Paris",
    "start_date": "2024-06-01",
    "end_date": "2024-06-07",
    "budget": 2000,
    "travelers_count": 2,
    "trip_type": "Couple",
    "accommodation_preference": "Hotel",
    "interests": ["culture", "food", "shopping"],
    "pace": "Balanced"
  }'
```

### 3. Flight Booking

```bash
# Search flights
curl -X POST "http://localhost:8000/api/v1/bookings/flights/search" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "NYC",
    "destination": "PAR", 
    "departure_date": "2024-06-01",
    "passengers": 2,
    "travel_class": "Economy"
  }'

# Book a flight
curl -X POST "http://localhost:8000/api/v1/bookings/flights/book" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "flight_id": "AI101",
    "passengers": [
      {
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-01",
        "gender": "Male",
        "nationality": "US"
      }
    ],
    "contact_email": "user@example.com",
    "contact_phone": "+1234567890",
    "emergency_contact": {"name": "Jane Doe", "phone": "+1234567891"}
  }'
```

### 4. Hotel Booking

```bash
# Search hotels
curl -X POST "http://localhost:8000/api/v1/bookings/hotels/search" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Paris",
    "check_in_date": "2024-06-01",
    "check_out_date": "2024-06-07",
    "guests": 2,
    "rooms": 1,
    "star_rating": 4
  }'
```

## Database Schema

The application uses SQLAlchemy ORM with the following main entities:

- **Users**: User accounts and profiles
- **Trips**: Trip planning and management
- **Destinations**: Travel destinations database
- **Bookings**: Booking records (flights, hotels, trains)
- **Flights/Hotels/Trains**: Specific booking details
- **Recommendations**: Travel recommendations
- **Weather**: Weather data cache

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection URL | `sqlite:///./travel_planner.db` |
| `SECRET_KEY` | JWT secret key | Required |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |
| `DEBUG` | Debug mode | `True` |
| `PORT` | Server port | `8000` |

### Database Options

**SQLite (Development)**
```
DATABASE_URL=sqlite:///./travel_planner.db
```

**PostgreSQL (Production)**
```
DATABASE_URL=postgresql://user:password@localhost/travel_planner
```

## Development

### Project Structure
```
backend/
├── main.py                 # FastAPI application entry
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── database.py            # Database configuration
├── auth.py                # Authentication utilities
└── routers/               # API route handlers
    ├── auth_router.py
    ├── trips_router.py
    ├── bookings_router.py
    ├── destinations_router.py
    └── ...
```

### Running Tests
```bash
pip install pytest pytest-asyncio
pytest
```

### Code Quality
```bash
# Install development dependencies
pip install black flake8 mypy

# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

## Production Deployment

### Docker Deployment
```dockerfile
# Dockerfile example
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Setup
1. Set secure `SECRET_KEY`
2. Configure production database
3. Set up proper CORS origins
4. Configure external API keys
5. Set up monitoring and logging

## Integration with External APIs

The backend is designed to integrate with:

- **OpenWeatherMap**: Weather data
- **Google Maps**: Location and mapping
- **Amadeus**: Flight booking APIs
- **Booking.com**: Hotel reservations
- **Railway APIs**: Train booking

## Security Features

- JWT token authentication
- Password hashing with bcrypt
- SQL injection prevention with SQLAlchemy ORM
- Input validation with Pydantic
- CORS configuration
- Rate limiting (can be added)

## Support & Contributing

For support or contributions:
1. Check the API documentation at `/docs`
2. Review the code structure
3. Follow the existing patterns for new features
4. Add tests for new functionality

## License

This project is for educational and demonstration purposes.