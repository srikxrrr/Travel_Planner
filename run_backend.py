#!/usr/bin/env python3
"""
Travel Planner Backend Startup Script
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import pydantic
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def setup_environment():
    """Setup environment variables"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found. Creating from example...")
        example_env = Path(".env.example")
        if example_env.exists():
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ Created .env file from .env.example")
            print("📝 Please edit .env file with your configuration")
        else:
            print("❌ .env.example file not found")
            return False
    return True

def run_backend():
    """Run the FastAPI backend"""
    print("🚀 Starting Travel Planner Backend...")
    print("📍 Backend will be available at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔄 Health Check: http://localhost:8000/api/v1/health")
    print("=" * 60)
    
    try:
        # Change to backend directory if it exists
        if Path("backend").exists():
            os.chdir("backend")
        
        # Run uvicorn server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 Backend stopped by user")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

def main():
    """Main function"""
    print("=" * 60)
    print("🌍 Travel Planner Backend")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Run backend
    run_backend()

if __name__ == "__main__":
    main()