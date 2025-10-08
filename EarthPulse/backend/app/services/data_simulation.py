"""
Realistic Environmental Data Simulation Service
Generates credible mock data that follows real-world environmental trends
"""

import random
import math
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import numpy as np

from app.models.environmental import (
    NDVIData, GlacierData, UrbanData, TemperatureData,
    EnvironmentalDataPoint, Region, DataIndicator, DataSource
)
from app.models.geographic import get_region_info, get_region_boundary, get_region_center
from app.config.settings import settings

logger = logging.getLogger(__name__)

class EnvironmentalDataSimulator:
    """Simulates realistic environmental data based on actual climate trends"""
    
    # Real-world data trends for Nepal Himalayas (2000-2025)
    REAL_TRENDS = {
        "ndvi": {
            "base_value": 0.65,
            "trend": 0.002,  # Slight improvement due to reforestation efforts
            "variation": 0.05,
            "seasonal_pattern": True
        },
        "glacier": {
            "initial_area": 1800.0,  # km² in 2000
            "retreat_rate": 25.0,  # km² per year
            "variation_fraction": 0.15,
            "acceleration_factor": 1.02  # Warming accelerates retreat
        },
        "urban": {
            "initial_area": 120.0,  # km² in 2000
            "growth_rate": 8.5,  # km² per year
            "variation_fraction": 0.20,
            "population_growth": 0.025  # 2.5% annual population growth
        },
        "temperature": {
            "base_temp": 17.5,  # Average temperature in 2000
            "warming_rate": 0.08,  # °C per year
            "variation": 1.5,
            "urban_heat_island": 1.2  # °C additional warming in urban areas
        }
    }
    
    def __init__(self):
        self.region_adjustments = self._calculate_region_adjustments()
    
    def _calculate_region_adjustments(self) -> Dict[str, Dict[str, float]]:
        """Calculate region-specific adjustments based on geographic characteristics"""
        return {
            "kathmandu_valley": {
                "ndvi": 0.8,  # Lower vegetation due to urbanization
                "glacier": 0.0,  # No glaciers in valley
                "urban": 2.5,  # Higher urban growth
                "temperature": 1.3  # Urban heat island effect
            },
            "annapurna_region": {
                "ndvi": 1.2,  # Higher vegetation at lower elevations
                "glacier": 1.5,  # Large glacier coverage
                "urban": 0.1,  # Minimal urban development
                "temperature": 0.7  # Mountain climate
            },
            "everest_region": {
                "ndvi": 0.3,  # Scarce vegetation at high altitude
                "glacier": 2.0,  # Major glacier systems
                "urban": 0.05,  # Virtually no urban areas
                "temperature": 0.4  # Extreme high altitude
            },
            "nepal_himalayas": {
                "ndvi": 1.0,  # Regional average
                "glacier": 1.0,  # Regional average
                "urban": 1.0,  # Regional average
                "temperature": 1.0  # Regional average
            }
        }
    
    async def simulate_ndvi_data(self, region: Region, year: int) -> NDVIData:
        """Simulate realistic NDVI data with NASA API integration"""
        await self._simulate_api_delay()
        
        # Try to fetch real NASA data first if not using mock data
        if not settings.USE_MOCK_DATA:
            try:
                from app.services.nasa_api import nasa_client
                real_data = await nasa_client.fetch_modis_ndvi(region.value, year)
                
                if real_data and real_data.get("data"):
                    # Process real NASA data
                    logger.info(f"Using real NASA MODIS data for {region.value} in {year}")
                    return self._process_real_ndvi_data(real_data, region, year)
                else:
                    logger.warning(f"No real NASA data available for {region.value} in {year}, falling back to simulation")
            except Exception as e:
                logger.error(f"Error fetching real NASA data: {e}, falling back to simulation")
        
        # Fall back to simulation
        logger.info(f"Using simulated NDVI data for {region.value} in {year}")
        trend_config = self.REAL_TRENDS["ndvi"]
        region_factor = self.region_adjustments[region.value]["ndvi"]
        
        # Calculate base NDVI value with trend
        years_from_2000 = year - 2000
        base_value = trend_config["base_value"] + (trend_config["trend"] * years_from_2000)
        base_value *= region_factor
        
        # Add realistic variation
        variation = random.uniform(-trend_config["variation"], trend_config["variation"])
        avg_ndvi = max(0.0, min(1.0, base_value + variation))
        
        # Calculate vegetation coverage
        vegetation_coverage = max(0, min(100, avg_ndvi * 85 + random.uniform(-5, 10)))
        
        # Generate trend
        if years_from_2000 > 15:  # Recent years show different trends
            trend = "increasing" if avg_ndvi > 0.6 else "stable"
        else:
            trend = "slightly_decreasing" if avg_ndvi < trend_config["base_value"] else "stable"
        
        region_info = get_region_info(region.value)
        if region_info:
            boundary = get_region_boundary(region.value)
            data_points = self._generate_spatial_data_points(
                boundary, "ndvi", avg_ndvi, trend_config["variation"], year
            )
        else:
            data_points = []
        
        return NDVIData(
            year=year,
            region=region,
            average_ndvi=round(avg_ndvi, 3),
            min_ndvi=round(max(0, avg_ndvi - trend_config["variation"]), 3),
            max_ndvi=round(min(1, avg_ndvi + trend_config["variation"]), 3),
            vegetation_coverage_percent=round(vegetation_coverage, 1),
            data_points=data_points,
            source=DataSource.MODIS,
            trend=trend
        )
    
    async def simulate_glacier_data(self, region: Region, year: int) -> GlacierData:
        """Simulate realistic glacier retreat data"""
        await self._simulate_api_delay()
        
        trend_config = self.REAL_TRENDS["glacier"]
        region_factor = self.region_adjustments[region.value]["glacier"]
        
        # Skip glaciers for regions without them
        if region_factor == 0:
            return GlacierData(
                year=year,
                region=region,
                glacier_area_km2=0.0,
                data_points=[],
                source=DataSource.SENTINEL,
                trend="none"
            )
        
        # Calculate glacier area with exponential retreat acceleration
        years_from_2000 = year - 2000
        
        # Calculate total retreat until this year
        total_retreat = sum([
            trend_config["retreat_rate"] * (trend_config["acceleration_factor"] ** y) 
            for y in range(years_from_2000 + 1)
        ])
        
        glacier_area = max(0, trend_config["initial_area"] - total_retreat) * region_factor
        
        # Add yearly variation
        variation_percent = random.uniform(
            -trend_config["variation_fraction"], 
            trend_config["variation_fraction"]
        )
        glacier_area *= (1 + variation_percent)
        
        # Estimate ice thickness
        base_thickness = 120 if glacier_area > 500 else 80
        thickness_variation = random.uniform(-10, 15)
        avg_thickness = base_thickness + thickness_variation
        
        region_info = get_region_info(region.value)
        if region_info:
            boundary = get_region_boundary(region.value)
            data_points = self._generate_spatial_data_points(
                boundary, "glacier", glacier_area / 100, 0.2, year
            )
        else:
            data_points = []
        
        return GlacierData(
            year=year,
            region=region,
            glacier_area_km2=round(glacier_area, 1),
            ice_thickness_m=round(max(0, avg_thickness), 1),
            retreat_rate_m_per_year=round(trend_config["retreat_rate"] / 20, 1),  # Rough conversion
            data_points=data_points,
            source=DataSource.SENTINEL,
            trend="decreasing"
        )
    
    async def simulate_urban_data(self, region: Region, year: int) -> UrbanData:
        """Simulate realistic urban expansion"""
        await self._simulate_api_delay()
        
        trend_config = self.REAL_TRENDS["urban"]
        region_factor = self.region_adjustments[region.value]["urban"]
        
        # Calculate cumulative urban area with growth
        years_from_2000 = year - 2000
        cumulative_growth = sum([
            trend_config["growth_rate"] * (1.01 ** y) 
            for y in range(years_from_2000)
        ])
        
        urban_area = trend_config["initial_area"] + cumulative_growth * region_factor
        
        # Add yearly variation
        variation_percent = random.uniform(
            -trend_config["variation_fraction"], 
            trend_config["variation_fraction"]
        )
        urban_area *= (1 + variation_percent)
        
        # Calculate built-up percentage based on region
        region_info = get_region_info(region.value)
        if region_info:
            total_area = region_info.area_km2
            built_up_percentage = (urban_area / total_area) * 100
            
            # Estimate population
            base_population = region_info.population or 100000
            population_growth = base_population * ((1 + trend_config["population_growth"]) ** years_from_2000)
            population_growth *= region_factor
            
            # Nightlight intensity correlates with urban density
            nightlight_intensity = min(100, built_up_percentage * 1.2 + random.uniform(-10, 15))
        else:
            built_up_percentage = 15.0
            population_growth = 500000
            nightlight_intensity = 20.0
        
        region_info = get_region_info(region.value)
        if region_info:
            boundary = get_region_boundary(region.value)
            data_points = self._generate_spatial_data_points(
                boundary, "urban", urban_area / 100, 0.25, year
            )
        else:
            data_points = []
        
        return UrbanData(
            year=year,
        region=region,
        urban_area_km2=round(max(0, urban_area), 1),
        built_up_percentage=round(built_up_percentage, 1),
        population_estimate=int(population_growth),
        nightlight_intensity=round(max(0, nightlight_intensity), 1),
        data_points=data_points,
        source=DataSource.LANDSAT,
        trend="expanding"
        )
    
    async def simulate_temperature_data(self, region: Region, year: int) -> TemperatureData:
        """Simulate realistic temperature warming"""
        await self._simulate_api_delay()
        
        trend_config = self.REAL_TRENDS["temperature"]
        region_factor = self.region_adjustments[region.value]["temperature"]
        
        # Calculate temperature with warming trend
        years_from_2000 = year - 2000
        base_temperature = trend_config["base_temp"] + (trend_config["warming_rate"] * years_from_2000)
        base_temperature *= region_factor
        
        # Add realistic seasonal and yearly variation
        yearly_variation = random.uniform(-trend_config["variation"], trend_config["variation"])
        avg_temp = base_temperature + yearly_variation
        
        # Calculate min/max temperatures
        temp_range = random.uniform(8, 15)
        min_temp = avg_temp - temp_range / 2
        max_temp = avg_temp + temp_range / 2
        
        # Urban heat island effect
        region_factor_val = self.region_adjustments[region.value]["temperature"]
        heat_island = trend_config["urban_heat_island"] if region_factor_val > 1.2 else 0.2
        
        region_info = get_region_info(region.value)
        if region_info:
            boundary = get_region_boundary(region.value)
            data_points = self._generate_spatial_data_points(
                boundary, "temperature", avg_temp, trend_config["variation"], year
            )
        else:
            data_points = []
        
        return TemperatureData(
            year=year,
            region=region,
            average_temperature_c=round(avg_temp, 1),
            min_temperature_c=round(min_temp, 1),
            max_temperature_c=round(max_temp, 1),
            heat_island_effect=round(heat_island, 1),
            data_points=data_points,
            source=DataSource.MODIS,
            trend="warming"
        )
    
    def _generate_spatial_data_points(
        self, 
        boundary: Optional[List[Tuple[float, float]]], 
        indicator_type: str, 
        base_value: float, 
        variation: float,
        year: int
    ) -> List[EnvironmentalDataPoint]:
        """Generate spatial data points across region"""
        if not boundary or len(boundary) < 3:
            return []
        
        # Generate sample points within region
        data_points = []
        num_points = random.randint(8, 25)
        
        # Get bounding box
        min_lng = min(point[0] for point in boundary)
        max_lng = max(point[0] for point in boundary)
        min_lat = min(point[1] for point in boundary)
        max_lat = max(point[1] for point in boundary)
        
        for _ in range(num_points):
            # Generate random points within bounding box
            longitude = random.uniform(min_lng, max_lng)
            latitude = random.uniform(min_lat, max_lat)
            
            # Add realistic variation to base value
            point_variation = random.uniform(-variation, variation)
            point_value = base_value + point_variation
            
            # Ensure reasonable bounds for different indicators
            if indicator_type == "ndvi":
                point_value = max(-1, min(1, point_value))
            elif indicator_type == "temperature":
                point_value = max(-50, min(50, point_value))
            elif indicator_type in ["glacier", "urban"]:
                point_value = max(0, point_value)
            
            confidence = random.uniform(0.75, 0.98)  # Simulate data confidence
            
            data_points.append(EnvironmentalDataPoint(
                longitude=longitude,
                latitude=latitude,
                value=round(point_value, 3),
                confidence=round(confidence, 2),
                timestamp=datetime(year, random.randint(6, 9), random.randint(1, 30))
            ))
        
        return data_points
    
    async def _simulate_api_delay(self):
        """Simulate realistic API response delays"""
        if settings.SIMULATE_API_DELAY:
            delay = random.uniform(
                settings.API_DELAY_MS * 0.5, 
                settings.API_DELAY_MS * 1.5
            ) / 1000
            await asyncio.sleep(delay)
    
    def _process_real_ndvi_data(self, real_data: dict, region: Region, year: int) -> NDVIData:
        """Process real NASA MODIS NDVI data"""
        try:
            # Extract data from NASA API response
            ndvi_values = real_data.get('data', [])
            if not ndvi_values:
                raise ValueError("No NDVI data in NASA response")
            
            # Calculate statistics
            values = [point['value'] for point in ndvi_values]
            avg_ndvi = sum(values) / len(values)
            min_ndvi = min(values)
            max_ndvi = max(values)
            
            # Calculate vegetation coverage
            vegetation_coverage = max(0, min(100, avg_ndvi * 85))
            
            # Generate data points
            data_points = [
                EnvironmentalDataPoint(
                    longitude=point['longitude'],
                    latitude=point['latitude'],
                    value=point['value'],
                    confidence=point.get('confidence', 0.95),
                    timestamp=point.get('timestamp', f"{year}-06-15T00:00:00Z")
                )
                for point in ndvi_values
            ]
            
            # Determine trend
            trend = "increasing" if avg_ndvi > 0.6 else "stable" if avg_ndvi > 0.3 else "decreasing"
            
            return NDVIData(
                year=year,
                region=region,
                average_ndvi=round(avg_ndvi, 3),
                min_ndvi=round(min_ndvi, 3),
                max_ndvi=round(max_ndvi, 3),
                vegetation_coverage_percent=round(vegetation_coverage, 1),
                data_points=data_points,
                source=DataSource.MODIS,
                trend=trend
            )
            
        except Exception as e:
            logger.error(f"Failed to process real NDVI data: {e}")
            # Fall back to simulation
            return self._simulate_ndvi_data_fallback(region, year)
    
    def _simulate_ndvi_data_fallback(self, region: Region, year: int) -> NDVIData:
        """Fallback NDVI simulation when real data fails"""
        trend_config = self.REAL_TRENDS["ndvi"]
        region_factor = self.region_adjustments[region.value]["ndvi"]
        
        years_from_2000 = year - 2000
        base_value = trend_config["base_value"] + (trend_config["trend"] * years_from_2000)
        base_value *= region_factor
        
        variation = random.uniform(-trend_config["variation"], trend_config["variation"])
        avg_ndvi = max(0.0, min(1.0, base_value + variation))
        vegetation_coverage = max(0, min(100, avg_ndvi * 85 + random.uniform(-5, 10)))
        
        region_info = get_region_info(region.value)
        if region_info:
            boundary = get_region_boundary(region.value)
            data_points = self._generate_spatial_data_points(
                boundary, "ndvi", avg_ndvi, trend_config["variation"], year
            )
        else:
            data_points = []
        
        trend = "increasing" if avg_ndvi > 0.6 else "stable"
        
        return NDVIData(
            year=year,
            region=region,
            average_ndvi=round(avg_ndvi, 3),
            min_ndvi=round(max(0, avg_ndvi - trend_config["variation"]), 3),
            max_ndvi=round(min(1, avg_ndvi + trend_config["variation"]), 3),
            vegetation_coverage_percent=round(vegetation_coverage, 1),
            data_points=data_points,
            source=DataSource.MODIS,
            trend=trend
        )

    def get_trend_summary(self, indicator: DataIndicator, region: Region, start_year: int, end_year: int) -> str:
        """Generate human-readable trend summary"""
        years = end_year - start_year
        
        summaries = {
            DataIndicator.NDVI: f"Vegetation health changed over {years} years in {region.value.replace('_', ' ').title()}",
            DataIndicator.GLACIER: f"Glacier coverage retreated significantly over {years} years in {region.value.replace('_', ' ').title()}",
            DataIndicator.URBAN: f"Urban areas expanded dramatically over {years} years in {region.value.replace('_', ' ').title()}",
            DataIndicator.TEMPERATURE: f"Temperatures warmed consistently over {years} years in {region.value.replace('_', ' ').title()}"
        }
        
        return summaries.get(indicator, "Environmental changes observed over time")

# Global simulator instance
environmental_simulator = EnvironmentalDataSimulator()