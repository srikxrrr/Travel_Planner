#!/usr/bin/env python3
"""
Simple test script to verify the travel planner backend is working
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def test_imports():
    """Test that all modules can be imported"""
    try:
        print("Testing imports...")
        
        # Test core modules
        import models
        import schemas
        import database
        import auth
        print("✅ Core modules imported successfully")
        
        # Test routers
        from routers import auth_router
        from routers import bookings_router
        from routers import trips_router
        from routers import destinations_router
        print("✅ Router modules imported successfully")
        
        # Test main app
        import main
        print("✅ Main app imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_schemas():
    """Test that schemas are properly defined"""
    try:
        print("\nTesting schemas...")
        from schemas import (
            UserCreate, FlightSearchRequest, HotelSearchRequest, 
            TrainSearchRequest, TripPlanningRequest
        )
        
        # Test UserCreate schema
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpassword123"
        }
        user = UserCreate(**user_data)
        print("✅ UserCreate schema works")
        
        # Test FlightSearchRequest schema
        flight_search = {
            "origin": "NYC",
            "destination": "LAX",
            "departure_date": "2024-06-01",
            "passengers": 2
        }
        flight = FlightSearchRequest(**flight_search)
        print("✅ FlightSearchRequest schema works")
        
        return True
    except Exception as e:
        print(f"❌ Schema error: {e}")
        return False

def test_app_creation():
    """Test that FastAPI app can be created"""
    try:
        print("\nTesting app creation...")
        from main import app
        
        # Check if app is created
        if app:
            print("✅ FastAPI app created successfully")
            print(f"✅ App title: {app.title}")
            print(f"✅ App version: {app.version}")
            return True
        else:
            print("❌ App creation failed")
            return False
    except Exception as e:
        print(f"❌ App creation error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Travel Planner Backend Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_schemas,
        test_app_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready to use.")
        print("\n📖 Next steps:")
        print("1. Run: python run_backend.py")
        print("2. Visit: http://localhost:8000/docs")
        print("3. Test the API endpoints")
        return True
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)