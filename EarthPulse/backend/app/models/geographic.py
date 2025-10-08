"""
Geographic Models for Earth Observation Visualizer
Regional boundaries, coordinates, and spatial data structures
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Tuple
from enum import Enum

class Coordinate(BaseModel):
    """Single coordinate point"""
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")

class BoundingBox(BaseModel):
    """Bounding box for geographic areas"""
    min_longitude: float = Field(..., ge=-180, le=180, description="Minimum longitude")
    min_latitude: float = Field(..., ge=-90, le=90, description="Minimum latitude")
    max_longitude: float = Field(..., ge=-180, le=180, description="Maximum longitude")
    max_latitude: float = Field(..., ge=-90, le=90, description="Maximum latitude")
    
    def get_center(self) -> Tuple[float, float]:
        """Get center coordinates of bounding box"""
        return (
            (self.min_longitude + self.max_longitude) / 2,
            (self.min_latitude + self.max_latitude) / 2
        )
    
    def get_width(self) -> float:
        """Get width of bounding box in degrees"""
        return self.max_longitude - self.min_longitude
    
    def get_height(self) -> float:
        """Get height of bounding box in degrees"""
        return self.max_latitude - self.min_latitude

class MapTile(BaseModel):
    """Map tile information"""
    z: int = Field(..., ge=0, le=18, description="Zoom level")
    x: int = Field(..., ge=0, description="Tile X coordinate")
    y: int = Field(..., ge=0, description="Tile Y coordinate")
    url: str = Field(..., description="Tile URL")
    tile_size: int = Field(default=256, description="Tile size in pixels")

class RegionInfo(BaseModel):
    """Detailed region information"""
    region_id: str = Field(..., description="Unique region identifier")
    name: str = Field(..., description="Region display name")
    coordinates: List[Coordinate] = Field(..., description="Region boundary coordinates")
    bounding_box: BoundingBox = Field(..., description="Region bounding box")
    area_km2: Optional[float] = Field(None, description="Region area in square kilometers")
    elevation_range: Optional[Tuple[float, float]] = Field(None, description="Min and max elevation in meters")
    population: Optional[int] = Field(None, description="Current population estimate")
    climate_zone: Optional[str] = Field(None, description="Climate classification")

# Predefined Nepal regions with actual coordinates
NEPAL_REGIONS = {
    "kathmandu_valley": RegionInfo(
        region_id="kathmandu_valley",
        name="Kathmandu Valley",
        coordinates=[
            Coordinate(longitude=85.2, latitude=27.6),
            Coordinate(longitude=85.4, latitude=27.6),
            Coordinate(longitude=85.4, latitude=27.8),
            Coordinate(longitude=85.2, latitude=27.8),
            Coordinate(longitude=85.2, latitude=27.6)
        ],
        bounding_box=BoundingBox(
            min_longitude=85.2,
            min_latitude=27.6,
            max_longitude=85.4,
            max_latitude=27.8
        ),
        area_km2=664,
        elevation_range=(1220, 2734),
        population=2500000,
        climate_zone="Subtropical Highland"
    ),
    
    "annapurna_region": RegionInfo(
        region_id="annapurna_region",
        name="Annapurna Region",
        coordinates=[
            Coordinate(longitude=83.8, latitude=28.1),
            Coordinate(longitude=84.6, latitude=28.1),
            Coordinate(longitude=84.6, latitude=28.8),
            Coordinate(longitude=83.8, latitude=28.8),
            Coordinate(longitude=83.8, latitude=28.1)
        ],
        bounding_box=BoundingBox(
            min_longitude=83.8,
            min_latitude=28.1,
            max_longitude=84.6,
            max_latitude=28.8
        ),
        area_km2=7629,
        elevation_range=(1000, 8091),
        population=130000,
        climate_zone="Alpine"
    ),
    
    "everest_region": RegionInfo(
        region_id="everest_region",
        name="Everest Region",
        coordinates=[
            Coordinate(longitude=86.6, latitude=27.7),
            Coordinate(longitude=87.3, latitude=27.7),
            Coordinate(longitude=87.3, latitude=28.3),
            Coordinate(longitude=86.6, latitude=28.3),
            Coordinate(longitude=86.6, latitude=27.7)
        ],
        bounding_box=BoundingBox(
            min_longitude=86.6,
            min_latitude=27.7,
            max_longitude=87.3,
            max_latitude=28.3
        ),
        area_km2=1148,
        elevation_range=(2000, 8848),
        population=15000,
        climate_zone="High Alpine"
    ),
    
    "nepal_himalayas": RegionInfo(
        region_id="nepal_himalayas",
        name="Entire Nepal Himalayas",
        coordinates=[
            Coordinate(longitude=80.0, latitude=26.0),
            Coordinate(longitude=88.5, latitude=26.0),
            Coordinate(longitude=88.5, latitude=30.5),
            Coordinate(longitude=80.0, latitude=30.5),
            Coordinate(longitude=80.0, latitude=26.0)
        ],
        bounding_box=BoundingBox(
            min_longitude=80.0,
            min_latitude=26.0,
            max_longitude=88.5,
            max_latitude=30.5
        ),
        area_km2=147181,
        elevation_range=(70, 8848),
        population=30000000,
        climate_zone="Diverse Alpine to Subtropical"
    )
}

def get_region_info(region_id: str) -> Optional[RegionInfo]:
    """Get region information by ID"""
    return NEPAL_REGIONS.get(region_id)

def get_region_boundary(region_id: str) -> Optional[List[Tuple[float, float]]]:
    """Get region boundary coordinates as tuples"""
    region = get_region_info(region_id)
    if region:
        return [(coord.longitude, coord.latitude) for coord in region.coordinates]
    return None

def get_region_center(region_id: str) -> Optional[Tuple[float, float]]:
    """Get region center coordinates"""
    region = get_region_info(region_id)
    if region:
        return region.bounding_box.get_center()
    return None
