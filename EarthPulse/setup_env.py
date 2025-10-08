#!/usr/bin/env python3
"""
Environment Setup Script for Earth Observation Visualizer
Creates .env files with proper NASA API configuration
"""

import os
from pathlib import Path

def create_backend_env():
    """Create backend .env file"""
    backend_env_content = """# Earth Observation Visualizer - Backend Environment Configuration
# NASA Earth Observation APIs
NASA_API_KEY=eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6IjAwOWFhZHUiLCJleHAiOjE3NjQ3NjgyOTksImlhdCI6MTc1OTU4NDI5OSwiaXNzIjoiaHR0cHM6Ly91cnMuZWFydGhkYXRhLm5hc2EuZ292IiwiaWRlbnRpdHlfcHJvdmlkZXIiOiJlZGxfb3BzIiwiYWNyIjoiZWRsIiwiYXNzdXJhbmNlX2xldmVsIjozfQ.5uCGUDoIYiVC-e3w43Q0JFmcY9uQBEMYakrHe0wh2piPGmwwyJ6-xiWLoxCV6giJHwBxguyUhrlWq6VrUVvEwsXH0OUun-YJkGI2Ak2fI6urZgqF6X05mNDxKB2VGl0ksTo6Xf_sEPHjnO12mwVA3S6WZDrYS6ujfJSdyeOXcksjzInABVwB8tPEZ7WHeC6SFjFqYTc3pNilplGoYdGngbJyiOKvoWvLsjLG8l5YMVNTKTuAIX7g0YtxvhNOaNNepPgNirwb9D1BKvhMQrHQFl_lLAo-80-oVZ9psXhspkAkRbFDnKQxC62qTfadRt6OvLmOSCGxtnEB4xyJodldzg
NASA_EO_BASE_URL=https://earthengine.googleapis.com/v1/
NASA_DISCOVERY_API=https://api.nasa.gov/access/data/
NASA_EARTH_DATA_API=https://earthengine.google.com/

# Google Earth Engine Configuration
GEE_PROJECT_ID=your_gee_project_id
GEE_ASSET_PATH=/v1/projects/your-project/assets

# Map Services APIs
CARTODB_API_KEY=your_cartodb_key_here
MAPBOX_TOKEN=your_mapbox_token_here
MAPBOX_STYLE_URL=mapbox://styles/mapbox/dark-v10

# NASA Data Catalogs
NASA_MODIS_API=https://lpdaacsvc.cr.usgs.gov/services/
NASA_LANDSAT_API=https://gsp.cr.usgs.gov/
NASA_SENTINEL_API=https://scihub.copernicus.eu/apihub/

# Application Settings
ENVIRONMENT=development
DEBUG=true
APP_NAME=Earth Observation Visualizer
APP_VERSION=1.0.0
HOST=0.0.0.0
PORT=8000

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/earth_obs_db
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=earth_obs_db
DATABASE_USER=earth_obs_user
DATABASE_PASSWORD=your_db_password

# Cache Configuration
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379

# Security
SECRET_KEY=your_secret_key_here_change_this_in_production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
ALLOWED_METHODS=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
ALLOWED_HEADERS=["*"]

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# Mock Data Configuration (Set to false for real NASA data)
USE_MOCK_DATA=false
MOCK_DATA_REGION=nepal_himalayas
SIMULATE_API_DELAY=true
API_DELAY_MS=500

# Environmental Data Configuration
DATA_YEAR_MIN=2000
DATA_YEAR_MAX=2025
DEFAULT_REGION=nepal_himalayas

# Processing Settings
MAX_CONCURRENT_REQUESTS=10
TIMEOUT_SECONDS=30
RETRY_ATTEMPTS=3

# File Storage
UPLOAD_DIR=./uploads
REPORT_OUTPUT_DIR=./reports
CACHE_DIR=./cache
MAX_FILE_SIZE=100MB

# API Rate Limiting
NASA_API_RATE_LIMIT=1000
MAP_API_RATE_LIMIT=50000
"""
    
    backend_env_path = Path("backend/.env")
    backend_env_path.write_text(backend_env_content)
    print("✅ Created backend/.env file")

def create_frontend_env():
    """Create frontend .env.local file"""
    frontend_env_content = """# Frontend Environment Configuration
# Backend API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_API_VERSION=v1
VITE_API_TIMEOUT=30000

# Development Flags
VITE_MOCK_DATA_ENABLED=false
VITE_DEBUG_MODE=true

# Map Services
VITE_MAPBOX_TOKEN=your_mapbox_token_here
VITE_CARTODB_API_KEY=your_cartodb_key_here

# Cache Configuration
VITE_CACHE_TTL=3600000
"""
    
    frontend_env_path = Path(".env.local")
    frontend_env_path.write_text(frontend_env_content)
    print("✅ Created .env.local file")

def create_directories():
    """Create necessary directories"""
    directories = [
        "backend/logs",
        "backend/uploads", 
        "backend/reports",
        "backend/cache",
        "backend/static"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def main():
    """Main setup function"""
    print("🌍 Earth Observation Visualizer - Environment Setup")
    print("=" * 60)
    
    try:
        create_directories()
        create_backend_env()
        create_frontend_env()
        
        print("\n🎉 Environment setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Start backend: cd backend && python -m uvicorn app.main:app --reload")
        print("2. Start frontend: npm run dev")
        print("3. Open http://localhost:3000 in your browser")
        print("\n🔧 Configuration files created:")
        print("- Backend: backend/.env")
        print("- Frontend: .env.local")
        print("\n🚀 NASA API is configured and ready to use!")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
