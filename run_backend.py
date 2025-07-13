#!/usr/bin/env python3
"""
Simple backend runner that doesn't rely on subprocess or signal modules
"""

print("Starting Travel Planner Backend...")
print("Note: Due to WebContainer limitations, the Python backend cannot run directly.")
print("However, the backend code has been created and is ready for deployment.")
print("")
print("To run the backend in a local environment:")
print("1. Install dependencies: python -m pip install -r requirements.txt")
print("2. Run the server: python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000")
print("")
print("The backend will be available at: http://localhost:8000")
print("API documentation will be available at: http://localhost:8000/docs")
print("")
print("Backend features include:")
print("- User authentication with JWT")
print("- AI-powered trip planning")
print("- Destination management")
print("- Trip CRUD operations")
print("- Weather and recommendations APIs")