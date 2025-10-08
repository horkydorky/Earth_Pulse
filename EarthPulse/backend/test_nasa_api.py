#!/usr/bin/env python3
"""
Test NASA API Integration
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.nasa_api import nasa_client
from app.config.settings import settings

async def test_nasa_api():
    """Test NASA API integration"""
    print("🌍 Testing NASA API Integration")
    print("=" * 50)
    
    # Test configuration
    print(f"NASA API Key: {settings.NASA_API_KEY[:20]}...")
    print(f"Use Mock Data: {settings.USE_MOCK_DATA}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print()
    
    # Initialize NASA client
    print("🚀 Initializing NASA API client...")
    await nasa_client.initialize()
    
    # Get API status
    print("📡 Getting API status...")
    status = await nasa_client.get_api_status()
    print(f"API Status: {status}")
    print()
    
    # Test NDVI data fetch
    print("🌱 Testing MODIS NDVI data fetch...")
    try:
        ndvi_data = await nasa_client.fetch_modis_ndvi("nepal_himalayas", 2020)
        if ndvi_data:
            print(f"✅ Successfully fetched NDVI data: {len(ndvi_data.get('data', []))} data points")
            print(f"Source: {ndvi_data.get('source', 'Unknown')}")
        else:
            print("⚠️ No NDVI data returned, will use simulation")
    except Exception as e:
        print(f"❌ Error fetching NDVI data: {e}")
    
    print("\n🎉 NASA API test completed!")

if __name__ == "__main__":
    asyncio.run(test_nasa_api())
