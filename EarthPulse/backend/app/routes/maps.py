"""
Map Services API Routes
Provides map tile endpoints and geographic data services
"""

from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Optional
from pydantic import BaseModel

from app.models.geographic import get_region_info, get_region_boundary, get_region_center
from app.models.environmental import Region
from app.config.settings import settings
from fastapi.responses import StreamingResponse
import httpx
import io

router = APIRouter()

class MapTileRequest(BaseModel):
    """Map tile request data"""
    z: int  # zoom level
    x: int  # tile x
    y: int  # tile y

class RegionMapData(BaseModel):
    """Region map data response"""
    region_id: str
    region_name: str
    center: Dict[str, float]  # {lng, lat}
    bounds: Dict[str, float]  # {min_lng, min_lat, max_lng, max_lat}
    coordinates: List[List[float]]  # [[lng, lat], ...]

@router.get("/regions")
async def get_regions():
    """Get all supported regions with their geographic data"""
    regions_data = []
    
    for region_id in ["nepal_himalayas", "kathmandu_valley", "annapurna_region", "everest_region"]:
        region_info = get_region_info(region_id)
        if region_info:
            boundary = get_region_boundary(region_id)
            center = get_region_center(region_id)
            
            regions_data.append(RegionMapData(
                region_id=region_id,
                region_name=region_info.name,
                center={"lng": center[0], "lat": center[1]} if center else {"lng": 0, "lat": 0},
                bounds={
                    "min_lng": region_info.bounding_box.min_longitude,
                    "min_lat": region_info.bounding_box.min_latitude,
                    "max_lng": region_info.bounding_box.max_longitude,
                    "max_lat": region_info.bounding_box.max_latitude
                },
                coordinates=boundary or []
            ))
    
    return {
        "regions": regions_data,
        "total_count": len(regions_data),
        "default_region": "nepal_himalayas"
    }

@router.get("/regions/{region_id}")
async def get_region_details(region_id: str):
    """Get detailed geographic information for a specific region"""
    if region_id not in ["nepal_himalayas", "kathmandu_valley", "annapurna_region", "everest_region"]:
        raise HTTPException(status_code=404, detail=f"Region '{region_id}' not found")
    
    region_info = get_region_info(region_id)
    if not region_info:
        raise HTTPException(status_code=500, detail="Region data not available")
    
    boundary = get_region_boundary(region_id)
    center = get_region_center(region_id)
    
    return {
        "region_id": region_id,
        "region_name": region_info.name,
        "description": f"Geographic region: {region_info.name}",
        "area": {
            "km2": region_info.area_km2,
            "description": f"Approximately {region_info.area_km2} square kilometers"
        },
        "population": {
            "estimate": region_info.population,
            "description": f"Estimated population: {region_info.population:,}"
        },
        "elevation": {
            "range": region_info.elevation_range,
            "description": f"Elevation range: {region_info.elevation_range[0]:.0f}m - {region_info.elevation_range[1]:.0f}m"
        },
        "climate": {
            "zone": region_info.climate_zone,
            "description": f"Climate: {region_info.climate_zone}"
        },
        "center": {"lng": center[0], "lat": center[1]} if center else {"lng": 0, "lat": 0},
        "bounds": {
            "min_lng": region_info.bounding_box.min_longitude,
            "min_lat": region_info.bounding_box.min_latitude,
            "max_lng": region_info.bounding_box.max_longitude,
            "max_lat": region_info.bounding_box.max_latitude
        },
        "coordinates": boundary or []
    }

@router.get("/tiles/{z}/{x}/{y}")
async def get_map_tile(z: int, x: int, y: int):
    """Generate or proxy map tiles for environmental visualization"""
    # Validate tile coordinates
    if z < 0 or z > 18:
        raise HTTPException(status_code=400, detail="Invalid zoom level")
    
    # For development, return placeholder tile information
    # In production, this would integrate with actual map tile services
    return {
        "z": z,
        "x": x,
        "y": y,
        "tile_url": f"https://api.mapbox.com/styles/v1/mapbox/dark-v10/tiles/{z}/{x}/{y}?access_token={settings.MAPBOX_TOKEN}",
        "attribution": "© OpenStreetMap contributors, © Mapbox",
        "license": "Development mode - Placeholder tile",
        "note": "Real map tiles will be generated when Mapbox token is configured"
    }

@router.get("/overlays")
async def get_environmental_overlays():
    """Get available environmental data overlay layers"""
    overlays = [
        {
            "id": "ndvi",
            "name": "Vegetation Index (NDVI)",
            "description": "Plant health and vegetation density",
            "source": "MODIS",
            "available_years": list(range(2000, 2026)),
            "color_scheme": {
                "min": "#8B4513",
                "max": "#228B22",
                "description": "Brown (low vegetation) to Green (high vegetation)"
            },
            "tile_template": "/api/v1/maps/overlays/ndvi/{year}/{z}/{x}/{y}"
        },
        {
            "id": "glacier",
            "name": "Glacier Coverage",
            "description": "Ice extent and glacier boundaries",
            "source": "Sentinel/Landsat",
            "available_years": list(range(2000, 2026)),
            "color_scheme": {
                "min": "#FFFFFF",
                "max": "#4169E1",
                "description": "White (ice) to Blue (significant coverage)"
            },
            "tile_template": "/api/v1/maps/overlays/glacier/{year}/{z}/{x}/{y}"
        },
        {
            "id": "urban",
            "name": "Urban Expansion",
            "description": "Built-up areas and urban development",
            "source": "Landsat/Nightlight",
            "available_years": list(range(2000, 2026)),
            "color_scheme": {
                "min": "#000080",
                "max": "#FFD700",
                "description": "Dark Blue (rural) to Gold (urban)"
            },
            "tile_template": "/api/v1/maps/overlays/urban/{year}/{z}/{x}/{y}"
        },
        {
            "id": "temperature",
            "name": "Land Surface Temperature",
            "description": "Surface temperature mapping",
            "source": "MODIS",
            "available_years": list(range(2000, 2026)),
            "color_scheme": {
                "min": "#0000FF",
                "max": "#FF0000",
                "description": "Blue (cool) to Red (warm)"
            },
            "tile_template": "/api/v1/maps/overlays/temperature/{year}/{z}/{x}/{y}"
        }
    ]
    
    return {
        "overlays": overlays,
        "total_count": len(overlays),
        "supported_zoom_levels": "0-15",
        "tile_size": 256,
        "attribution": "Environmental data overlays for Nepal Himalayan region"
    }

@router.get("/overlays/{indicator}/{year}/{z}/{x}/{y}")
async def get_environmental_overlay_tile(
    indicator: str,
    year: int,
    z: int,
    x: int,
    y: int
):
    """Generate environmental data overlay tile"""
    
    # Validate inputs
    if indicator not in ["ndvi", "glacier", "urban", "temperature"]:
        raise HTTPException(status_code=400, detail="Invalid indicator")
    
    if year < settings.DATA_YEAR_MIN or year > settings.DATA_YEAR_MAX:
        raise HTTPException(status_code=400, detail="Year out of range")
    
    if z < 0 or z > 15:
        raise HTTPException(status_code=400, detail="Invalid zoom level")
    
    # For development, return placeholder information
    # In production, this would generate actual environmental data tiles
    return {
        "indicator": indicator,
        "year": year,
        "z": z,
        "x": x,
        "y": y,
        "status": "placeholder",
        "message": "Environmental overlay tiles will be generated with real NASA satellite data",
        "development_note": "Configure NASA API endpoint to enable real tile generation"
    }

@router.get("/styles")
async def get_map_styles():
    """Get available map styles for environmental visualization"""
    styles = [
        {
            "id": "dark",
            "name": "Dark Theme",
            "description": "Dark theme optimized for environmental data visualization",
            "url": "https://api.mapbox.com/styles/v1/mapbox/dark-v10/tiles/{z}/{x}/{y}?access_token={token}",
            "attribution": "© OpenStreetMap contributors, © Mapbox",
            "recommended_for": ["Environmental data overlays", "Night imagery", "Scientific visualization"]
        },
        {
            "id": "satellite",
            "name": "Satellite Imagery",
            "description": "High-resolution satellite imagery",
            "url": "https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/{z}/{x}/{y}?access_token={token}",
            "attribution": "© Mapbox, © Maxar Technologies",
            "recommended_for": ["Current state visualization", "High-resolution analysis", "Ground truth"]
        },
        {
            "id": "venue",
            "name": "Light Theme",
            "description": "Light theme for reports and presentations",
            "url": "https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/{z}/{x}/{y}?access_token={token}",
            "attribution": "© OpenStreetMap contributors, © Mapbox",
            "recommended_for": ["Reports", "Presentations", "Print publications"]
        }
    ]
    
    return {
        "styles": styles,
        "default_style": "dark",
        "environmental_recommended": ["dark", "satellite"],
        "note": "Configure Mapbox token to enable real map tiles"
    }

@router.get("/configuration")
async def get_map_configuration():
    """Get default map configuration for the application"""
    return {
        "default_view": {
            "center": [85.3240, 27.7172],  # Nepal center
            "zoom": 7,
            "region": "nepal_himalayas"
        },
        "max_bounds": {
            "northeast": [88.5, 30.5],
            "southwest": [80.0, 26.0]
        },
        "controls": {
            "fullscreen": True,
            "zoom": True,
            "attribution": True,
            "geolocation": False,
            "scale": True
        },
        "overlays": {
            "default_opacity": 0.7,
            "max_opacity": 1.0,
            "min_opacity": 0.3
        },
        "tiles": {
            "size": 256,
            "format": "png",
            "cache_duration": "30d"
        },
        "environmental_indicators": {
            "default_years": [2000, 2005, 2010, 2015, 2020, 2025],
            "animation_interval": 2000,
            "auto_play": False
        },
        "supported_formats": ["png", "jpeg", "geotiff"],
        "api_status": "mock_mode",
        "real_integration": "Ready for NASA Earth Observation API"
    }

@router.get("/placeholder/{width}/{height}")
async def get_placeholder_image(width: int, height: int):
    """Serve a simple placeholder image for storytelling snapshots"""
    from PIL import Image, ImageDraw

    w = max(32, min(2000, width))
    h = max(32, min(2000, height))

    img = Image.new('RGB', (w, h), color=(10, 25, 45))
    draw = ImageDraw.Draw(img)

    # Decorative frame
    draw.rectangle([(4, 4), (w - 5, h - 5)], outline=(56, 189, 248), width=2)
    # Title text (fallback if fonts unavailable)
    try:
        draw.text((12, 12), "Satellite Snapshot", fill=(199, 210, 254))
        draw.text((12, 36), "Development Placeholder", fill=(147, 197, 253))
    except Exception:
        pass

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")

@router.get("/gibs/snapshot")
async def get_gibs_snapshot(
    layer: str = Query(default="MODIS_Terra_NDVI_16Day", description="GIBS layer name"),
    year: int = Query(default=2020, ge=settings.DATA_YEAR_MIN, le=settings.DATA_YEAR_MAX),
    month: int = Query(default=6, ge=1, le=12),
    day: int = Query(default=15, ge=1, le=31),
    width: int = Query(default=600, ge=64, le=2000),
    height: int = Query(default=400, ge=64, le=2000),
    bbox: str = Query(default="26,80,30.5,88.5", description="minLat,minLon,maxLat,maxLon for EPSG:4326")
):
    """Proxy a NASA GIBS WMS GetMap image for a given date and region.
    Defaults to Nepal Himalayas bbox and 600x400 size. No Mapbox required.
    """
    # Validate bbox format
    try:
        parts = [float(x) for x in bbox.split(",")]
        if len(parts) != 4:
            raise ValueError
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid bbox format. Use 'minLat,minLon,maxLat,maxLon'")

    date_str = f"{year:04d}-{month:02d}-{day:02d}"
    # GIBS best WMS in EPSG:4326
    base_url = "https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi"
    params = {
        "service": "WMS",
        "request": "GetMap",
        "version": "1.3.0",
        "layers": layer,
        "styles": "",
        "format": "image/png",
        "transparent": "true",
        "height": str(height),
        "width": str(width),
        "crs": "EPSG:4326",
        "bbox": bbox,
        "time": date_str
    }

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(base_url, params=params)
            if resp.status_code != 200 or not resp.headers.get("Content-Type", "").startswith("image/"):
                raise HTTPException(status_code=502, detail=f"GIBS error: {resp.status_code}")
            return StreamingResponse(io.BytesIO(resp.content), media_type=resp.headers.get("Content-Type", "image/png"))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch GIBS image: {e}")
