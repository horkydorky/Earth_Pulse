"""
Environmental Data API Routes
Provides endpoints for NDVI, Glacier, Urban, and Temperature data
"""

from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional, Union
from datetime import datetime

from app.models.environmental import (
    NDVIData, GlacierData, UrbanData, TemperatureData,
    DataIndicator, Region, EnvironmentalSummary, ComparisonResult
)
from app.services.data_simulation import environmental_simulator
from app.config.settings import settings

router = APIRouter()

@router.get("/ndvi/{year}", response_model=NDVIData)
async def get_ndvi_data(
    year: int = Path(..., ge=settings.DATA_YEAR_MIN, le=settings.DATA_YEAR_MAX),
    region: Region = Query(default=Region.NEPAL_HIMALAYAS, description="Geographic region")
):
    """
    Get NDVI (Vegetation Index) data for a specific year and region
    
    - **year**: Year between 2000-2025
    - **region**: Geographic region (nepal_himalayas, kathmandu_valley, annapurna_region, everest_region)
    """
    # Always delegate to simulator which will use real NASA data when configured,
    # and gracefully fallback to simulated data otherwise.
    return await environmental_simulator.simulate_ndvi_data(region, year)

@router.get("/glacier/{year}", response_model=GlacierData)
async def get_glacier_data(
    year: int = Path(..., ge=settings.DATA_YEAR_MIN, le=settings.DATA_YEAR_MAX),
    region: Region = Query(default=Region.NEPAL_HIMALAYAS, description="Geographic region")
):
    """
    Get Glacier coverage and retreat data for a specific year and region
    
    - **year**: Year between 2000-2025
    - **region**: Geographic region (nepal_himalayas, kathmandu_valley, annapurna_region, everest_region)
    """
    return await environmental_simulator.simulate_glacier_data(region, year)

@router.get("/urban/{year}", response_model=UrbanData)
async def get_urban_data(
    year: int = Path(..., ge=settings.DATA_YEAR_MIN, le=settings.DATA_YEAR_MAX),
    region: Region = Query(default=Region.NEPAL_HIMALAYAS, description="Geographic region")
):
    """
    Get Urban expansion data for a specific year and region
    
    - **year**: Year between 2000-2025
    - **region**: Geographic region (nepal_himalayas, kathmandu_valley, annapurna_region, everest_region)
    """
    return await environmental_simulator.simulate_urban_data(region, year)

@router.get("/temperature/{year}", response_model=TemperatureData)
async def get_temperature_data(
    year: int = Path(..., ge=settings.DATA_YEAR_MIN, le=settings.DATA_YEAR_MAX),
    region: Region = Query(default=Region.NEPAL_HIMALAYAS, description="Geographic region")
):
    """
    Get Land Surface Temperature data for a specific year and region
    
    - **year**: Year between 2000-2025
    - **region**: Geographic region (nepal_himalayas, kathmandu_valley, annapurna_region, everest_region)
    """
    return await environmental_simulator.simulate_temperature_data(region, year)

@router.get("/summary", response_model=EnvironmentalSummary)
async def get_environmental_summary(
    year: int = Query(..., ge=settings.DATA_YEAR_MIN, le=settings.DATA_YEAR_MAX),
    region: Region = Query(default=Region.NEPAL_HIMALAYAS, description="Geographic region")
):
    """
    Get comprehensive environmental summary for all indicators in a specific year and region
    
    - **year**: Year between 2000-2025
    - **region**: Geographic region (nepal_himalayas, kathmandu_valley, annapurna_region, everest_region)
    """
    # Generate all environmental data concurrently (real or simulated handled in service)
    import asyncio
    
    ndvi_task = environmental_simulator.simulate_ndvi_data(region, year)
    glacier_task = environmental_simulator.simulate_glacier_data(region, year)
    urban_task = environmental_simulator.simulate_urban_data(region, year)
    temperature_task = environmental_simulator.simulate_temperature_data(region, year)
    
    ndvi_data, glacier_data, urban_data, temperature_data = await asyncio.gather(
        ndvi_task, glacier_task, urban_task, temperature_task
    )
    
    return EnvironmentalSummary(
        year=year,
        region=region,
        ndvi_data=ndvi_data,
        glacier_data=glacier_data,
        urban_data=urban_data,
        temperature_data=temperature_data
    )

@router.get("/compare/temporal", response_model=List[ComparisonResult])
async def get_temporal_comparison(
    indicator: DataIndicator = Query(..., description="Environmental indicator to compare"),
    region: Region = Query(default=Region.NEPAL_HIMALAYAS, description="Geographic region"),
    start_year: int = Query(default=2000, ge=settings.DATA_YEAR_MIN, le=settings.DATA_YEAR_MAX),
    end_year: int = Query(default=2025, ge=settings.DATA_YEAR_MIN, le=settings.DATA_YEAR_MAX),
    include_intermediate: bool = Query(default=False, description="Include data for years between start and end")
):
    """
    Compare environmental data across different years
    
    - **indicator**: Environmental indicator (ndvi, glacier, urban, temperature)
    - **region**: Geographic region (nepal_himalayas, kathmandu_valley, annapurna_region, everest_region)
    - **start_year**: Starting year for comparison (2000-2025)
    - **end_year**: Ending year for comparison (2000-2025)
    - **include_intermediate**: Include data for in-between years
    """
    if start_year >= end_year:
        raise HTTPException(status_code=400, detail="start_year must be less than end_year")
    
    results = []
    years_to_analyze = [start_year, end_year]
    
    if include_intermediate:
        # Include every 5 years in between
        intermediate_years = list(range(start_year + 5, end_year, 5))
        years_to_analyze = sorted([start_year] + intermediate_years + [end_year])
    
    # Get data for comparison years
    import asyncio
    
    async def get_indicator_data(year: int):
        if indicator == DataIndicator.NDVI:
            return await environmental_simulator.simulate_ndvi_data(region, year)
        elif indicator == DataIndicator.GLACIER:
            return await environmental_simulator.simulate_glacier_data(region, year)
        elif indicator == DataIndicator.URBAN:
            return await environmental_simulator.simulate_urban_data(region, year)
        elif indicator == DataIndicator.TEMPERATURE:
            return await environmental_simulator.simulate_temperature_data(region, year)
    
    data_tasks = [get_indicator_data(y) for y in years_to_analyze]
    data_results = await asyncio.gather(*data_tasks)
    
    # Calculate comparison metrics
    baseline_data = data_results[0]
    comparison_data = data_results[-1]
    
    # Extract baseline values based on indicator type
    if indicator == DataIndicator.NDVI:
        baseline_value = baseline_data.average_ndvi
        comparison_value = comparison_data.average_ndvi
    elif indicator == DataIndicator.GLACIER:
        baseline_value = baseline_data.glacier_area_km2
        comparison_value = comparison_data.glacier_area_km2
    elif indicator == DataIndicator.URBAN:
        baseline_value = baseline_data.urban_area_km2
        comparison_value = comparison_data.urban_area_km2
    elif indicator == DataIndicator.TEMPERATURE:
        baseline_value = baseline_data.average_temperature_c
        comparison_value = comparison_data.average_temperature_c
    
    change_amount = comparison_value - baseline_value
    change_percentage = (change_amount / baseline_value * 100) if baseline_value != 0 else 0
    
    trend_summary = environmental_simulator.get_trend_summary(indicator, region, start_year, end_year)
    
    result = ComparisonResult(
        comparison_type="temporal",
        region=region,
        indicator=indicator,
        baseline_year=start_year,
        comparison_year=end_year,
        baseline_value=round(baseline_value, 3),
        comparison_value=round(comparison_value, 3),
        change_amount=round(change_amount, 3),
        change_percentage=round(change_percentage, 2),
        trend_summary=trend_summary,
        impact_assessment=f"The {indicator.value} indicator shows significant change over {end_year - start_year} years"
    )
    
    return [result]

@router.get("/indicators")
async def get_supported_indicators():
    """Get list of supported environmental indicators"""
    return {
        "indicators": [
            {
                "id": "ndvi",
                "name": "Normalized Difference Vegetation Index",
                "description": "Plant health and vegetation density",
                "unit": "NDVI",
                "source": "MODIS/Landsat",
                "range": "0.0 to 1.0"
            },
            {
                "id": "glacier",
                "name": "Glacier Coverage",
                "description": "Glacier extent and ice coverage",
                "unit": "km²",
                "source": "Sentinel/Landsat",
                "range": "Variable"
            },
            {
                "id": "urban",
                "name": "Urban Expansion",
                "description": "Built-up area and urban development",
                "unit": "km²",
                "source": "Landsat/Nightlight",
                "range": "Variable"
            },
            {
                "id": "temperature",
                "name": "Land Surface Temperature",
                "description": "Surface temperature monitoring",
                "unit": "°C",
                "source": "MODIS",
                "range": "Variable"
            }
        ],
        "regions": [
            {
                "id": "nepal_himalayas",
                "name": "Nepal Himalayas",
                "description": "Entire Nepal Himalayan region"
            },
            {
                "id": "kathmandu_valley",
                "name": "Kathmandu Valley",
                "description": "Urban valley region"
            },
            {
                "id": "annapurna_region",
                "name": "Annapurna Region",
                "description": "Mountain region with glaciers"
            },
            {
                "id": "everest_region",
                "name": "Everest Region",
                "description": "High altitude extreme environment"
            }
        ]
    }

@router.get("/trends/{indicator}", response_model=List[dict])
async def get_indicator_trends(
    indicator: DataIndicator = Path(..., description="Environmental indicator"),
    region: Region = Query(default=Region.NEPAL_HIMALAYAS, description="Geographic region"),
    year_range: str = Query(default="2000-2025", description="Year range in format 'start-end'")
):
    """
    Get historical trends for an environmental indicator
    
    - **indicator**: Environmental indicator (ndvi, glacier, urban, temperature)
    - **region**: Geographic region
    - **year_range**: Year range in format '2000-2025'
    """
    try:
        start_year, end_year = map(int, year_range.split("-"))
        if start_year < settings.DATA_YEAR_MIN or end_year > settings.DATA_YEAR_MAX:
            raise ValueError("Year range out of bounds")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid year range format. Use 'YYYY-YYYY'")
    
    # Generate data for every 5 years
    years = list(range(start_year, end_year + 1, 5))
    if years[-1] != end_year:
        years.append(end_year)
    
    import asyncio
    
    async def get_trend_data(year: int):
        if indicator == DataIndicator.NDVI:
            data = await environmental_simulator.simulate_ndvi_data(region, year)
            return {
                "year": year,
                "value": data.average_ndvi,
                "unit": "NDVI",
                "trend": data.trend
            }
        elif indicator == DataIndicator.GLACIER:
            data = await environmental_simulator.simulate_glacier_data(region, year)
            return {
                "year": year,
                "value": data.glacier_area_km2,
                "unit": "km²",
                "trend": data.trend
            }
        elif indicator == DataIndicator.URBAN:
            data = await environmental_simulator.simulate_urban_data(region, year)
            return {
                "year": year,
                "value": data.urban_area_km2,
                "unit": "km²",
                "trend": data.trend
            }
        elif indicator == DataIndicator.TEMPERATURE:
            data = await environmental_simulator.simulate_temperature_data(region, year)
            return {
                "year": year,
                "value": data.average_temperature_c,
                "unit": "°C",
                "trend": data.trend
            }
    
    trend_data = await asyncio.gather(*[get_trend_data(y) for y in years])
    
    return sorted(trend_data, key=lambda x: x["year"])
