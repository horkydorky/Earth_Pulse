"""
Earth Observation Visualizer - FastAPI Main Application
Integrates NASA Earth Observation data for environmental visualization
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from typing import Dict, Any
import logging

# Import routes
from app.routes import environmental, maps, reports
from app.config.settings import settings 

# Configure logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events"""
    # Startup
    logger.info("🌍 Earth Observation Visualizer Backend Starting...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    logger.info(f"Using Mock Data: {settings.USE_MOCK_DATA}")
    
    # Initialize any required services here
    await initialize_services()
    
    yield
    
    # Shutdown
    logger.info("🌍 Earth Observation Visualizer Backend Shutting Down...")

async def initialize_services():
    """Initialize external services and connections"""
    try:
        # Initialize NASA API connections
        from app.services.nasa_api import NASAEOClient
        nasa_client = NASAEOClient()
        await nasa_client.initialize()
        logger.info("✅ NASA API Client initialized")
        
        # Initialize map services
        from app.services.map_service import MapService
        map_service = MapService()
        await map_service.initialize()
        logger.info("✅ Map Service initialized")
        
        logger.info("🚀 All services initialized successfully")
    except Exception as e:
        logger.error(f"❌ Error initializing services: {e}")
        # Don't raise the error, just log it and continue
        # The app can still work with mock data
        logger.info("🔄 Continuing with mock data mode")

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Interactive Earth Observation Visualizer using NASA satellite data for environmental change analysis",
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# Include API routes
app.include_router(environmental.router, prefix="/api/v1/environmental", tags=["Environmental Data"])
app.include_router(maps.router, prefix="/api/v1/maps", tags=["Map Services"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports & Export"])

@app.get("/")
async def root():
    """Root endpoint with application information"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "environment": settings.ENVIRONMENT,
        "data_source": "Mock Data (NASA EO Simulation)" if settings.USE_MOCK_DATA else "NASA Earth Observation APIs",
        "endpoints": {
            "docs": "/api/docs" if settings.DEBUG else "Documentation disabled in production",
            "environmental": "/api/v1/environmental",
            "maps": "/api/v1/maps",
            "reports": "/api/v1/reports"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T01:01:01Z",
        "services": {
            "nasa_api": "operational",
            "map_service": "operational",
            "database": "operational" if not settings.USE_MOCK_DATA else "mock",
            "redis_cache": "operational" if not settings.USE_MOCK_DATA else "mock"
        }
    }

@app.get("/api/v1/info")
async def api_info():
    """API information and capabilities"""
    return {
        "api_version": "v1",
        "capabilities": [
            "Environmental indicator tracking (NDVI, Glaciers, Urban, Temperature)",
            "Temporal data analysis (2000-2025)",
            "Regional comparison tools",
            "Map tile generation",
            "Report generation and export",
            "Real-time data simulation"
        ],
        "data_indicators": {
            "ndvi": "Normalized Difference Vegetation Index (MODIS)",
            "glacier": "Glacier coverage and retreat analysis",
            "urban": "Urban expansion using nightlight data",
            "temperature": "Land surface temperature (LST)"
        },
        "geographic_coverage": [
            "Nepal Himalayas",
            "Kathmandu Valley",
            "Annapurna Region",
            "Everest Region"
        ],
        "integration_ready": True,
        "real_api_endpoint": "Ready for NASA Earth Observation API integration"
    }

@app.get("/api/v1/environmental/summary")
async def environmental_summary():
    """Summary endpoint for environmental data"""
    return {
        "summary": "This is a summary of environmental data",
        "details": "More details about the environmental data"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "detailed_message": str(exc) if settings.DEBUG else "Debug mode disabled"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
