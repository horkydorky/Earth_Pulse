"""
Environmental Data Models for Earth Observation Visualizer
Based on NASA Earth Observation datasets
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

class DataIndicator(str, Enum):
    """Environmental data indicators"""
    NDVI = "ndvi"
    GLACIER = "glacier"
    URBAN = "urban"
    TEMPERATURE = "temperature"

class Region(str, Enum):
    """Supported geographic regions"""
    NEPAL_HIMALAYAS = "nepal_himalayas"
    KATHMANDU_VALLEY = "kathmandu_valley"
    ANNAPURNA_REGION = "annapurna_region"
    EVEREST_REGION = "everest_region"

class DataSource(str, Enum):
    """Environmental data sources"""
    MODIS = "modis"
    LANDSAT = "landsat"
    SENTINEL = "sentinel"
    OTHER = "other"

class EnvironmentalDataPoint(BaseModel):
    """Single environmental data point"""
    longitude: float = Field(..., description="Longitude coordinate")
    latitude: float = Field(..., description="Latitude coordinate")
    value: float = Field(..., description="Environmental measurement value")
    confidence: Optional[float] = Field(None, description="Data confidence level (0-1)")
    timestamp: datetime = Field(..., description="Measurement timestamp")
    
class NDVIData(BaseModel):
    """NDVI (Normalized Difference Vegetation Index) data"""
    year: int = Field(..., ge=2000, le=2025, description="Year of measurement")
    region: Region = Field(..., description="Geographic region")
    average_ndvi: float = Field(..., ge=-1, le=1, description="Average NDVI value")
    min_ndvi: float = Field(..., ge=-1, le=1, description="Minimum NDVI value")
    max_ndvi: float = Field(..., ge=-1, le=1, description="Maximum NDVI value")
    vegetation_coverage_percent: float = Field(..., ge=0, le=100, description="Vegetation coverage percentage")
    data_points: List[EnvironmentalDataPoint] = Field(default_factory=list)
    source: DataSource = Field(default=DataSource.MODIS, description="Data source")
    trend: Optional[str] = Field(None, description="Trend direction: increasing/decreasing/stable")

class GlacierData(BaseModel):
    """Glacier coverage and retreat data"""
    year: int = Field(..., ge=2000, le=2025, description="Year of measurement")
    region: Region = Field(..., description="Geographic region")
    glacier_area_km2: float = Field(..., ge=0, description="Glacier area in square kilometers")
    ice_thickness_m: Optional[float] = Field(None, description="Average ice thickness in meters")
    retreat_rate_m_per_year: Optional[float] = Field(None, description="Annual retreat rate")
    data_points: List[EnvironmentalDataPoint] = Field(default_factory=list)
    source: DataSource = Field(default=DataSource.SENTINEL, description="Data source")
    trend: Optional[str] = Field(None, description="Trend direction: increasing/decreasing/ stable")

class UrbanData(BaseModel):
    """Urban expansion data"""
    year: int = Field(..., ge=2000, le=2025, description="Year of measurement")
    region: Region = Field(..., description="Geographic region")
    urban_area_km2: float = Field(..., ge=0, description="Urban area in square kilometers")
    built_up_percentage: float = Field(..., ge=0, le=100, description="Built-up area percentage")
    population_estimate: Optional[int] = Field(None, description="Estimated population")
    nightlight_intensity: Optional[float] = Field(None, description="Average nightlight intensity")
    data_points: List[EnvironmentalDataPoint] = Field(default_factory=list)
    source: DataSource = Field(default=DataSource.LANDSAT, description="Data source")
    trend: Optional[str] = Field(None, description="Trend direction: expanding/contracting/stable")

class TemperatureData(BaseModel):
    """Land surface temperature data"""
    year: int = Field(..., ge=2000, le=2025, description="Year of measurement")
    region: Region = Field(..., description="Geographic region")
    average_temperature_c: float = Field(..., description="Average temperature in Celsius")
    min_temperature_c: float = Field(..., description="Minimum temperature in Celsius")
    max_temperature_c: float = Field(..., description="Maximum temperature in Celsius")
    heat_island_effect: Optional[float] = Field(None, description="Urban heat island intensity")
    data_points: List[EnvironmentalDataPoint] = Field(default_factory=list)
    source: DataSource = Field(default=DataSource.MODIS, description="Data source")
    trend: Optional[str] = Field(None, description="Trend direction: warming/cooling/stable")

class TemporalComparison(BaseModel):
    """Temporal comparison data for multiple years"""
    indicator: DataIndicator = Field(..., description="Environmental indicator")
    region: Region = Field(..., description="Geographic region")
    start_year: int = Field(..., ge=2000, le=2025, description="Start year of comparison")
    end_year: int = Field(..., ge=2000, le=2025, description="End year of comparison")
    change_percentage: float = Field(..., description="Percentage change over period")
    change_value: float = Field(..., description="Absolute change value")
    trend_direction: str = Field(..., description="Direction of change")
    confidence_level: float = Field(..., ge=0, le=1, description="Statistical confidence")
    
class RegionalBoundary(BaseModel):
    """Regional boundary coordinates"""
    region: Region = Field(..., description="Region identifier")
    coordinates: List[List[float]] = Field(..., description="Boundary coordinates [[lng,lat], ...]")
    bounding_box: Dict[str, float] = Field(..., description="Bounding box: {min_lng, min_lat, max_lng, max_lat}")
    center: Dict[str, float] = Field(..., description="Region center: {lng, lat}")
    
class EnvironmentalSummary(BaseModel):
    """Summary environmental data for a region and year"""
    year: int = Field(..., ge=2000, le=2025, description="Year")
    region: Region = Field(..., description="Geographic region")
    ndvi_data: Optional[NDVIData] = None
    glacier_data: Optional[GlacierData] = None
    urban_data: Optional[UrbanData] = None
    temperature_data: Optional[TemperatureData] = None
    
class ComparisonResult(BaseModel):
    """Comparison result between two periods or regions"""
    comparison_type: str = Field(..., description="Type of comparison: temporal or regional")
    region: Region = Field(..., description="Geographic region")
    indicator: DataIndicator = Field(..., description="Environmental indicator")
    baseline_year: Optional[int] = Field(None, ge=2000, le=2025)
    comparison_year: Optional[int] = Field(None, ge=2000, le=2025)
    baseline_value: float = Field(..., description="Baseline measurement value")
    comparison_value: float = Field(..., description="Comparison measurement value")
    change_amount: float = Field(..., description="Absolute change")
    change_percentage: float = Field(..., description="Percentage change")
    trend_summary: str = Field(..., description="Human-readable trend summary")
    impact_assessment: Optional[str] = Field(None, description="Assessment of environmental impact")

class DataValidation(BaseModel):
    """Data quality and validation information"""
    completeness: float = Field(..., ge=0, le=100, description="Data completeness percentage")
    accuracy: float = Field(..., ge=0, le=1, description="Data accuracy score")
    spatial_resolution: str = Field(..., description="Spatial resolution of data")
    temporal_resolution: str = Field(..., description="Temporal resolution of data")
    last_updated: datetime = Field(..., description="Last data update timestamp")
    data_gaps: List[str] = Field(default_factory=list, description="Identified data gaps")
