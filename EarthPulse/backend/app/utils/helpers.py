"""
Helper utilities for Earth Observation Visualizer
Common functions, data processing, and utilities
"""

import hashlib
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import math

def generate_cache_key(*args: Any) -> str:
    """Generate cache key from arguments"""
    key_string = "_".join(str(arg) for arg in args)
    return hashlib.md5(key_string.encode()).hexdigest()

def validate_year(year: int, min_year: int = 2000, max_year: int = 2025) -> bool:
    """Validate year is within supported range"""
    return min_year <= year <= max_year

def validate_coordinates(latitude: float, longitude: float) -> bool:
    """Validate geographic coordinates"""
    return -90 <= latitude <= 90 and -180 <= longitude <= 180

def interpolate_value(value1: float, value2: float, ratio: float) -> float:
    """Linear interpolation between two values"""
    return value1 + (value2 - value1) * ratio

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates using Haversine formula"""
    
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def normalize_ndvi(ndvi: float) -> float:
    """Normalize NDVI value to 0-1 range"""
    return max(-1, min(1, ndvi))

def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32

def km2_to_miles2(km2: float) -> float:
    """Convert square kilometers to square miles"""
    return km2 * 0.386102

def format_number(value: float, decimals: int = 2) -> str:
    """Format number with specified decimal places"""
    return f"{value:.{decimals}f}"

def format_percentage(value: float, decimals: int = 1) -> str:
    """Format number as percentage"""
    return f"{value:.{decimals}f}%"

def format_large_number(value: int) -> str:
    """Format large numbers as K/M/B"""
    
    if value >= 1000000000:
        return f"{value/1000000000:.1f}B"
    elif value >= 1000000:
        return f"{value/1000000:.1f}M"
    elif value >= 1000:
        return f"{value/1000:.1f}K"
    else:
        return str(value)

def get_trend_symbol(trend: str) -> str:
    """Get visual symbol for trend direction"""
    
    symbols = {
        "increasing": "↗",
        "decreasing": "↘", 
        "stable": "→",
        "expanding": "↗",
        "contracting": "↘",
        "warming": "↗",
        "cooling": "↘",
        "rising": "↗",
        "falling": "↘", 
        "none": "-"
    }
    
    return symbols.get(trend.lower(), "→")

def get_trend_color(trend: str, indicator: str) -> str:
    """Get color for trend visualization"""
    
    trend_lower = trend.lower()
    
    # Different colors based on indicator type
    if indicator in ["ndvi", "vegetation"]:
        return "green" if "increasing" in trend_lower else "red"
    elif indicator in ["glacier"]:
        return "red" if "decreasing" in trend_lower else "green"
    elif indicator in ["urban", "built_up"]:
        return "orange" if "expanding" in trend_lower else "blue"
    elif indicator in ["temperature"]:
        return "red" if "warming" in trend_lower else "blue"
    else:
        return "gray"

def create_summary_statistics(values: List[float]) -> Dict[str, float]:
    """Create summary statistics from list of values"""
    
    if not values:
        return {}
    
    sorted_values = sorted(values)
    n = len(values)
    
    return {
        "mean": sum(values) / n,
        "median": sorted_values[n//2] if n % 2 == 0 else (sorted_values[n//2] + sorted_values[n//2 + 1]) / 2,
        "min": min(values),
        "max": max(values),
        "range": max(values) - min(values),
        "std_dev": math.sqrt(sum((x - sum(values)/n)**2 for x in values) / n) if n > 0 else 0
    }

def mask_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Mask sensitive data in environment variables"""
    
    sensitive_keys = ["api_key", "token", "password", "secret"]
    masked_data = data.copy()
    
    for key, value in masked_data.items():
        if any(sensitive in key.lower() for sensitive in sensitive_keys):
            if isinstance(value, str) and len(value) > 8:
                masked_data[key] = value[:4] + "*" * (len(value) - 8) + value[-4:]
            else:
                masked_data[key] = "***"
    
    return masked_data

def generate_file_timestamp() -> str:
    """Generate timestamp for file naming"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def validate_email(email: str) -> bool:
    """Simple email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def safe_json_serializer(obj: Any) -> str:
    """Safe JSON serializer that handles various data types"""
    
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, set):
        return list(obj)
    elif hasattr(obj, 'dict'):  # Pydantic models
        return obj.dict()
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes)):
        return list(obj)
    else:
        return str(obj)

def create_data_validation_summary(
    data_count: int,
    completeness: float,
    accuracy: float,
    last_update: datetime
) -> Dict[str, Any]:
    """Create data validation summary"""
    
    return {
        "data_points": data_count,
        "completeness_percent": round(completeness, 1),
        "accuracy_score": round(accuracy, 2),
        "last_updated": last_update.isoformat(),
        "validation_status": "high_confidence" if completeness > 90 and accuracy > 0.8 else "medium_confidence" if completeness > 70 else "low_confidence"
    }

def extract_coordinate_bounds(coordinates: List[Tuple[float, float]]) -> Dict[str, float]:
    """Extract bounding box from list of coordinates"""
    
    if not coordinates:
        return {}
    
    lats = [coord[1] for coord in coordinates]
    lons = [coord[0] for coord in coordinates]
    
    return {
        "min_longitude": min(lons),
        "min_latitude": min(lats),
        "max_longitude": max(lons),
        "max_latitude": max(lats)
    }

def time_series_interpolation(
    values: List[float], 
    timestamps: List[datetime],
    target_time: datetime
) -> Optional[float]:
    """Interpolate time series value at target time"""
    
    if len(values) != len(timestamps) or len(values) == 0:
        return None
    
    # Find surrounding data points
    for i in range(len(timestamps) - 1):
        if timestamps[i] <= target_time <= timestamps[i + 1]:
            # Linear interpolation
            ratio = (target_time - timestamps[i]).total_seconds() / (timestamps[i + 1] - timestamps[i]).total_seconds()
            return interpolate_value(values[i], values[i + 1], ratio)
    
    return None

def create_cache_configuration() -> Dict[str, Any]:
    """Create cache configuration for environment data"""
    
    return {
        "cache_version": "1.0",
        "cache_strategy": "time_based_invalidation",
        "default_ttl_seconds": 3600,  # 1 hour
        "environmental_data_ttl": 86400,  # 24 hours
        "map_tiles_ttl": 604800,  # 7 days
        "report_cache_ttl": 1800,  # 30 minutes
        "max_cache_size_mb": 1000,
        "compression": True,
        "serialization_format": "json"
    }

# Common data transformations
def transform_indicator_name(indicator: str) -> str:
    """Transform indicator identifier to display name"""
    
    transformations = {
        "ndvi": "Vegetation Index",
        "glacier": "Glacier Coverage", 
        "urban": "Urban Expansion",
        "temperature": "Surface Temperature"
    }
    
    return transformations.get(indicator.lower(), indicator.title())

def transform_region_name(region: str) -> str:
    """Transform region identifier to display name"""
    
    transformations = {
        "nepal_himalayas": "Nepal Himalayas",
        "kathmandu_valley": "Kathmandu Valley",
        "annapurna_region": "Annapurna Region", 
        "everest_region": "Everest Region"
    }
    
    return transformations.get(region.lower(), region.replace('_', ' ').title())
