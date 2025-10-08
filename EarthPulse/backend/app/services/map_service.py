"""
Map Services Integration
Provides integration with map tile services and geographic data
"""

import httpx
import asyncio
from typing import Dict, List, Optional, Tuple, Any
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class MapService:
    """Map Services Integration for tiles and geographic data"""
    
    def __init__(self):
        self.cartodb_key = settings.CARTODB_API_KEY
        self.mapbox_token = settings.MAPBOX_TOKEN
        self.mapbox_style_url = settings.MAPBOX_STYLE_URL
        self.client = None
        self.is_initialized = False
    
    async def initialize(self):
        """Initialize map service client"""
        try:
            # Initialize HTTP client for map services
            self.client = httpx.AsyncClient(
                timeout=30.0,
                headers={
                    "User-Agent": "Earth-Observation-Visualizer/1.0"
                }
            )
            
            # Verify map service availability
            if self.mapbox_token != "your_mapbox_token_here":
                # Test Mapbox service
                response = await self.client.get(
                    f"https://api.mapbox.com/styles/v1/mapbox/dark-v10/tiles/0/0/0?access_token={self.mapbox_token}"
                )
                if response.status_code == 200:
                    logger.info("Mapbox service initialized successfully")
                    self.is_initialized = True
                else:
                    logger.warning(f"Mapbox service test failed: {response.status_code}")
            
            if self.cartodb_key != "your_cartodb_key_here":
                # Test CartoDB service
                base_url = "https://{s}.basemaps.cartocdn.com/dark_all"
                response = await self.client.get(base_url.format(s="a") + "/0/0/0.png")
                if response.status_code == 200:
                    logger.info("CartoDB service initialized successfully")
                    self.is_initialized = True
                else:
                    logger.warning(f"CartoDB service test failed: {response.status_code}")
            
            if not self.is_initialized:
                logger.info("Map services not configured, using placeholder tiles")
                self.is_initialized = True
                
        except Exception as e:
            logger.error(f"Failed to initialize map services: {e}")
            self.is_initialized = False
    
    async def generate_environmental_tile(
        self,
        indicator: str,
        year: int,
        z: int,
        x: int,
        y: int
    ) -> Optional[bytes]:
        """Generate environmental data overlay tile"""
        
        try:
            # TODO: Implement real environmental tile generation
            # For now, return placeholder tile data
            
            # In production, this would:
            # 1. Fetch environmental data for the tile area
            # 2. Generate appropriate color mapping
            # 3. Create PNG tile image
            # 4. Return tile bytes
            
            logger.info(f"Generating {indicator} tile for {year} at z:{z}, x:{x}, y:{y}")
            
            # Placeholder tile generation
            placeholder_tile_path = await self._generate_placeholder_tile(
                indicator, year, z, x, y
            )
            
            return placeholder_tile_path
            
        except Exception as e:
            logger.error(f"Failed to generate environmental tile: {e}")
            return None
    
    async def get_tile_url(
        self,
        tile_type: str,
        z: int,
        x: int,
        y: int,
        style: str = "dark"
    ) -> str:
        """Get map tile URL for the specified parameters"""
        
        if tile_type == "satellite":
            if self.mapbox_token == "your_mapbox_token_here":
                return f"/api/v1/maps/placeholder/{z}/{x}/{y}"
            return f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/{z}/{x}/{y}?access_token={self.mapbox_token}"
        
        elif tile_type == "dark":
            if self.mapbox_token == "your_mapbox_token_here":
                return f"/api/v1/maps/placeholder/{z}/{x}/{y}"
            return f"https://api.mapbox.com/styles/v1/mapbox/dark-v10/tiles/{z}/{x}/{y}?access_token={self.mapbox_token}"
        
        elif tile_type == "light":
            if self.mapbox_token == "your_mapbox_token_here":
                return f"/api/v1/maps/placeholder/{z}/{x}/{y}"
            return f"https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/{z}/{x}/{y}?access_token={self.mapbox_token}"
        
        elif tile_type == "cartodb_dark":
            return f"https://{{s}}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png"
        
        else:
            # Default to CartoDB dark theme
            return f"https://{{s}}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png"
    
    async def get_attribution_info(self, tile_type: str) -> Dict[str, str]:
        """Get attribution information for map tiles"""
        
        attributions = {
            "satellite": {
                "attribution": "© Mapbox, © Maxar Technologies",
                "license": "Mapbox Satellite Imagery License"
            },
            "dark": {
                "attribution": "© OpenStreetMap contributors, © Mapbox",
                "license": "Mapbox Design License"
            },
            "light": {
                "attribution": "© OpenStreetMap contributors, © Mapbox", 
                "license": "Mapbox Design License"
            },
            "cartodb_dark": {
                "attribution": "© OpenStreetMap contributors, © CARTO",
                "license": "ODbl"
            }
        }
        
        return attributions.get(tile_type, {
            "attribution": "© OpenStreetMap contributors",
            "license": "ODbl"
        })
    
    async def _generate_placeholder_tile(
        self,
        indicator: str,
        year: int,
        z: int,
        x: int,
        y: int
    ) -> bytes:
        """Generate placeholder tile for environmental data"""
        
        # Generate simple colored tile based on indicator
        import io
        from PIL import Image, ImageDraw
        
        # Create 256x256 tile
        size = 256
        image = Image.new('RGB', (size, size), color=self._get_indicator_color(indicator))
        draw = ImageDraw.Draw(image)
        
        # Add grid overlay to simulate data points
        grid_size = 32
        opacity = Image.new('RGB', (size, size), (0, 0, 0, 50))
        
        # Draw grid
        for i in range(0, size, grid_size):
            draw.line([(i, 0), (i, size)], fill=(255, 255, 255, 100), width=1)
        for i in range(0, size, grid_size):
            draw.line([(0, i), (size, i)], fill=(255, 255, 255, 100), width=1)
        
        # Add indicator text
        try:
            # This might fail if PIL doesn't have font support
            draw.text((10, 10), f"{indicator.upper()}", fill=(255, 255, 255))
            draw.text((10, 30), f"{year}", fill=(255, 255, 255))
            draw.text((10, 50), f"z:{z} x:{x} y:{y}", fill=(255, 255, 255))
        except:
            pass
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return img_byte_arr.getvalue()
    
    def _get_indicator_color(self, indicator: str) -> Tuple[int, int, int]:
        """Get color for environmental indicator"""
        
        colors = {
            "ndvi": (34, 139, 34),      # Green for vegetation
            "glacier": (176, 224, 230), # Light blue for glaciers
            "urban": (255, 165, 0),     # Orange for urban
            "temperature": (255, 69, 0)  # Red for temperature
        }
        
        return colors.get(indicator.lower(), (128, 128, 128))  # Gray default
    
    async def get_service_status(self) -> Dict[str, Any]:
        """Get map service status"""
        
        return {
            "status": "operational" if self.is_initialized else "not_initialized",
            "cartodb_configured": self.cartodb_key != "your_cartodb_key_here",
            "mapbox_configured": self.mapbox_token != "your_mapbox_token_here",
            "client_initialized": self.client is not None,
            "services": {
                "cartodb_dark": "Available",
                "mapbox_satellite": "Available" if self.mapbox_token != "your_mapbox_token_here" else "Not configured",
                "mapbox_dark": "Available" if self.mapbox_token != "your_mapbox_token_here" else 'Not configured',
                "mapbox_light": "Available" if self.mapbox_token != "your_mapbox_token_here" else "Not configured"
            },
            "tile_generation": "Placeholder tiles" if not self.client else "Real tile generation"
        }
    
    async def close(self):
        """Close map service client"""
        if self.client:
            await self.client.aclose()
            self.client = None
            self.is_initialized = False

# Global map service instance
map_service = MapService()
