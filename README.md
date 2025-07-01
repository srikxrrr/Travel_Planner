# 🌍 Travel Planner - Complete Booking & Planning Platform

A comprehensive travel planning and booking platform with a modern React frontend and powerful FastAPI backend. Features flight, hotel, and train booking systems with AI-powered trip planning.

![Travel Planner](https://img.shields.io/badge/Travel-Planner-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)
![React](https://img.shields.io/badge/React-18.2.0-blue)
![Python](https://img.shields.io/badge/Python-3.9+-yellow)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue)

## ✨ Features

### 🎯 **Complete Booking System**
- ✈️ **Flight Booking** - Search, compare, and book flights with multiple airlines
- 🏨 **Hotel Reservations** - Find and book accommodations with detailed filters
- 🚆 **Train Tickets** - Book train tickets with seat/berth selection
- 💳 **Payment Processing** - Secure payment handling with multiple methods
- 📱 **Booking Management** - Track, modify, and cancel bookings

### 🗺️ **Smart Trip Planning**
- 🤖 **AI-Powered Itineraries** - Personalized travel plans based on interests
- 📅 **Multi-Day Planning** - Detailed day-by-day activity scheduling
- 💰 **Budget Estimation** - Smart cost calculation and tracking
- 🌟 **Recommendations** - Local attractions, restaurants, and activities
- ⚡ **Real-time Weather** - Weather forecasts for destinations

### 🔐 **User Management**
- 👤 **User Authentication** - Secure JWT-based login system
- 📊 **User Profiles** - Personalized preferences and history
- 🔄 **Social Features** - Trip sharing and collaboration
- 📈 **Analytics** - Travel statistics and insights

## 🏗️ Architecture

```
Travel Planner/
├── 🎨 Frontend (React + TypeScript)
│   ├── Modern UI with Tailwind CSS
│   ├── Responsive design
│   ├── Interactive booking flows
│   └── Real-time updates
│
└── ⚡ Backend (FastAPI + Python)
    ├── RESTful API with auto-docs
    ├── JWT Authentication
    ├── Database with SQLAlchemy
    ├── Booking management
    └── External API integrations
```

## 🚀 Quick Start

### Prerequisites
- **Node.js** 16+ and npm
- **Python** 3.9+ and pip
- **PostgreSQL** (optional, SQLite for development)

### 1. Clone Repository
```bash
git clone https://github.com/your-username/travel-planner.git
cd travel-planner
```

### 2. Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Start backend
python run_backend.py
```

### 3. Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Access Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📖 API Documentation

The backend provides a comprehensive REST API with automatic documentation:

### 🔐 Authentication Endpoints
```
POST /api/v1/auth/register    # User registration
POST /api/v1/auth/login       # User login
GET  /api/v1/auth/me          # Current user info
PUT  /api/v1/auth/me          # Update profile
```

### 🎯 Trip Planning Endpoints
```
POST /api/v1/trips/plan       # Generate AI trip plan
POST /api/v1/trips/           # Create trip
GET  /api/v1/trips/           # Get user trips
GET  /api/v1/trips/{id}       # Get trip details
PUT  /api/v1/trips/{id}       # Update trip
```

### 📋 Booking Endpoints
```
POST /api/v1/bookings/flights/search    # Search flights
POST /api/v1/bookings/flights/book      # Book flight
POST /api/v1/bookings/hotels/search     # Search hotels
POST /api/v1/bookings/hotels/book       # Book hotel
POST /api/v1/bookings/trains/search     # Search trains
POST /api/v1/bookings/trains/book       # Book train
GET  /api/v1/bookings/my-bookings       # Get bookings
```

## 🛠️ Technology Stack

### Frontend
- **React 18** - Modern UI library
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Vite** - Fast build tool
- **Lucide React** - Beautiful icons

### Backend
- **FastAPI** - High-performance API framework
- **SQLAlchemy** - Powerful ORM
- **JWT** - Secure authentication
- **Pydantic** - Data validation
- **PostgreSQL/SQLite** - Database options

### DevOps & Tools
- **GitHub Actions** - CI/CD pipeline
- **Docker** - Containerization
- **Pytest** - Testing framework
- **Black** - Code formatting

## 🎨 Screenshots

### Trip Planning Interface
```
🗺️ Interactive destination search and selection
📅 Calendar-based date picker
🎯 Interest-based activity recommendations
💰 Real-time budget calculation
```

### Booking Flow
```
✈️ Flight search with filters and sorting
🏨 Hotel listing with photos and amenities
🚆 Train selection with seat/berth mapping
💳 Secure payment processing
📧 Booking confirmation and e-tickets
```

## 🔧 Development

### Backend Development
```bash
cd backend

# Run tests
python test_backend.py

# Code formatting
black .

# Type checking
mypy .

# Start with auto-reload
uvicorn main:app --reload
```

### Frontend Development
```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Linting
npm run lint
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python test_backend.py
pytest  # Unit tests
```

### Frontend Tests
```bash
npm test
npm run test:coverage
```

## 🐳 Docker Deployment

### Using Docker Compose
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Individual Services
```bash
# Backend only
docker build -t travel-planner-backend ./backend
docker run -p 8000:8000 travel-planner-backend

# Frontend only
docker build -t travel-planner-frontend .
docker run -p 3000:3000 travel-planner-frontend
```

## 🌐 Environment Configuration

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost/travel_planner
SECRET_KEY=your-secret-key-here
OPENWEATHERMAP_API_KEY=your-api-key
AMADEUS_API_KEY=your-api-key
```

### Frontend (.env.local)
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_GOOGLE_MAPS_API_KEY=your-api-key
```

## 📈 Features Roadmap

### Phase 1 ✅
- [x] User authentication system
- [x] Basic trip planning
- [x] Flight/hotel/train booking
- [x] Payment processing simulation
- [x] Responsive UI design

### Phase 2 🚧
- [ ] Real-time booking with external APIs
- [ ] Advanced trip collaboration
- [ ] Mobile app development
- [ ] Push notifications
- [ ] Offline mode support

### Phase 3 📋
- [ ] AI-powered recommendations
- [ ] Social features and reviews
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] Enterprise features

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Process
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass
6. Submit a pull request

### Code Style
- Follow existing code patterns
- Use TypeScript for frontend
- Follow PEP 8 for Python
- Add proper documentation
- Include unit tests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 **Documentation**: Check the `/docs` folder
- 🐛 **Bug Reports**: Open an issue on GitHub
- 💬 **Discussions**: Use GitHub Discussions
- 📧 **Email**: support@travelplanner.com

## 🙏 Acknowledgments

- **FastAPI** - For the excellent API framework
- **React** - For the powerful UI library
- **Tailwind CSS** - For the utility-first CSS framework
- **SQLAlchemy** - For the robust ORM
- **All Contributors** - For making this project better

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/your-username/travel-planner)
![GitHub forks](https://img.shields.io/github/forks/your-username/travel-planner)
![GitHub issues](https://img.shields.io/github/issues/your-username/travel-planner)
![GitHub license](https://img.shields.io/github/license/your-username/travel-planner)

---

**Made with ❤️ by the Travel Planner Team**

[⭐ Star this repo](https://github.com/your-username/travel-planner) | [🐛 Report Bug](https://github.com/your-username/travel-planner/issues) | [💡 Request Feature](https://github.com/your-username/travel-planner/issues)