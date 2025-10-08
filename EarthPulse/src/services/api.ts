/**
 * Earth Observation Visualizer API Service
 * Handles communication with backend FastAPI services
 */

// Environment variables with safe fallback to current host:8000
const API_BASE_URL = ((): string => {
  const envUrl = (import.meta as any)?.env?.VITE_API_BASE_URL
  if (envUrl && typeof envUrl === 'string') return envUrl
  if (typeof window !== 'undefined') {
    return `${window.location.protocol}//${window.location.hostname}:8000`
  }
  return 'http://localhost:8000'
})()
const API_VERSION = import.meta.env.VITE_API_VERSION || 'v1'
const API_TIMEOUT = parseInt(import.meta.env.VITE_API_TIMEOUT || '30000')

// Types for environmental data
export interface EnvironmentalDataPoint {
  longitude: number
  latitude: number
  value: number
  confidence?: number
  timestamp: string
}

export interface NDVIData {
  year: number
  region: string
  average_ndvi: number
  min_ndvi: number
  max_ndvi: number
  vegetation_coverage_percent: number
  data_points: EnvironmentalDataPoint[]
  source: string
  trend: string
}

export interface GlacierData {
  year: number
  region: string
  glacier_area_km2: number
  ice_thickness_m?: number
  retreat_rate_m_per_year?: number
  data_points: EnvironmentalDataPoint[]
  source: string
  trend: string
}

export interface UrbanData {
  year: number
  region: string
  urban_area_km2: number
  built_up_percentage: number
  population_estimate?: number
  nightlight_intensity?: number
  data_points: EnvironmentalDataPoint[]
  source: string
  trend: string
}

export interface TemperatureData {
  year: number
  region: string
  average_temperature_c: number
  min_temperature_c: number
  max_temperature_c: number
  heat_island_effect?: number
  data_points: EnvironmentalDataPoint[]
  source: string
  trend: string
}

export interface EnvironmentalSummary {
  year: number
  region: string
  ndvi_data?: NDVIData
  glacier_data?: GlacierData
  urban_data?: UrbanData
  temperature_data?: TemperatureData
}

export interface ComparisonResult {
  comparison_type: string
  region: string
  indicator: string
  baseline_year?: number
  comparison_year?: number
  baseline_value: number
  comparison_value: number
  change_amount: number
  change_percentage: number
  trend_summary: string
  impact_assessment?: string
}

export interface RegionInfo {
  region_id: string
  region_name: string
  center: { lng: number; lat: number }
  bounds: { min_lng: number; min_lat: number; max_lng: number; max_lat: number }
  coordinates: number[][]
}

export interface ReportRequest {
  report_type?: string
  year?: number
  region?: string
  indicators?: string[]
  include_charts?: boolean
  include_maps?: boolean
  language?: string
}

export interface ExportRequest {
  format: string
  indicators: string[]
  region?: string
  start_year?: number
  end_year?: number
  include_raw_data?: boolean
}

// API Client Class
class EOApiClient {
  private baseURL: string

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = `${baseURL}/api/${API_VERSION}`
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`
    
    const defaultOptions: RequestInit = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    }

    const config = {
      ...defaultOptions,
      ...options,
      headers: {
        ...defaultOptions.headers,
        ...options.headers,
      },
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error)
      throw error
    }
  }

  // Environmental Data API Methods
  async getNDVIData(year: number, region: string = 'nepal_himalayas'): Promise<NDVIData> {
    return this.request<NDVIData>(
      `/environmental/ndvi/${year}?region=${region}`
    )
  }

  async getGlacierData(year: number, region: string = 'nepal_himalayas'): Promise<GlacierData> {
    return this.request<GlacierData>(
      `/environmental/glacier/${year}?region=${region}`
    )
  }

  async getUrbanData(year: number, region: string = 'nepal_himalayas'): Promise<UrbanData> {
    return this.request<UrbanData>(
      `/environmental/urban/${year}?region=${region}`
    )
  }

  async getTemperatureData(year: number, region: string = 'nepal_himalayas'): Promise<TemperatureData> {
    return this.request<TemperatureData>(
      `/environmental/temperature/${year}?region=${region}`
    )
  }

  async getEnvironmentalSummary(year: number, region: string = 'nepal_himalayas'): Promise<EnvironmentalSummary> {
    return this.request<EnvironmentalSummary>(
      `/environmental/summary?year=${year}&region=${region}`
    )
  }

  async getTemporalComparison(
    indicator: string,
    region: string = 'nepal_himalayas',
    startYear: number = 2000,
    endYear: number = 2025,
    includeIntermediate: boolean = false
  ): Promise<ComparisonResult[]> {
    const params = new URLSearchParams({
      indicator,
      region,
      start_year: startYear.toString(),
      end_year: endYear.toString(),
      include_intermediate: includeIntermediate.toString()
    })
    
    return this.request<ComparisonResult[]>(
      `/environmental/compare/temporal?${params}`
    )
  }

  async getIndicatorTrends(
    indicator: string,
    region: string = 'nepal_himalayas',
    yearRange: string = '2000-2025'
  ): Promise<any[]> {
    return this.request<any[]>(
      `/environmental/trends/${indicator}?region=${region}&year_range=${yearRange}`
    )
  }

  // Map Services API Methods
  async getRegions(): Promise<{ regions: RegionInfo[] }> {
    return this.request<{ regions: RegionInfo[] }>('/maps/regions')
  }

  async getRegionDetails(regionId: string): Promise<any> {
    return this.request<any>(`/maps/regions/${regionId}`)
  }

  async getMapConfiguration(): Promise<any> {
    return this.request<any>('/maps/configuration')
  }

  async getMapStyles(): Promise<any> {
    return this.request<any>('/maps/styles')
  }

  async getEnvironmentalOverlays(): Promise<any> {
    return this.request<any>('/maps/overlays')
  }

  // Reports API Methods
  async generateReport(request: ReportRequest): Promise<any> {
    return this.request<any>('/reports/generate', {
      method: 'POST',
      body: JSON.stringify(request)
    })
  }

  async downloadReport(reportId: string): Promise<any> {
    return this.request<any>(`/reports/download/${reportId}`)
  }

  async exportData(request: ExportRequest): Promise<any> {
    return this.request<any>('/reports/export', {
      method: 'POST',
      body: JSON.stringify(request)
    })
  }

  async getSupportedFormats(): Promise<any> {
    return this.request<any>('/reports/formats')
  }

  // Health Check
  async getHealthStatus(): Promise<any> {
    return this.request<any>('/health')
  }

  async getApiInfo(): Promise<any> {
    return this.request<any>('/info')
  }
}

// Cache implementation for environmental data
class DataCache {
  private cache: Map<string, any> = new Map()
  private ttl: Map<string, number> = new Map()
  private defaultTTL: number = parseInt(import.meta.env.VITE_CACHE_TTL || '3600000') // 1 hour

  set(key: string, value: any, customTTL?: number): void {
    const ttl = customTTL || this.defaultTTL
    this.cache.set(key, value)
    this.ttl.set(key, Date.now() + ttl)
  }

  get(key: string): any | null {
    const expiry = this.ttl.get(key)
    if (!expiry) return null
    
    if (Date.now() > expiry) {
      this.cache.delete(key)
      this.ttl.delete(key)
      return null
    }
    
    return this.cache.get(key) || null
  }

  clear(): void {
    this.cache.clear()
    this.ttl.clear()
  }

  delete(key: string): void {
    this.cache.delete(key)
    this.ttl.delete(key)
  }
}

// Enhanced API Client with caching
export class EOApiService {
  private client: EOApiClient
  private cache: DataCache

  constructor() {
    this.client = new EOApiClient()
    this.cache = new DataCache()
  }

  // Cached methods for better performance
  async getNDVIData(year: number, region: string = 'nepal_himalayas'): Promise<NDVIData> {
    const cacheKey = `ndvi_${year}_${region}`
    const cachedData = this.cache.get(cacheKey)
    
    if (cachedData) {
      return cachedData
    }
    
    const data = await this.client.getNDVIData(year, region)
    this.cache.set(cacheKey, data)
    return data
  }

  async getGlacierData(year: number, region: string = 'nepal_himalayas'): Promise<GlacierData> {
    const cacheKey = `glacier_${year}_${region}`
    const cachedData = this.cache.get(cacheKey)
    
    if (cachedData) {
      return cachedData
    }
    
    const data = await this.client.getGlacierData(year, region)
    this.cache.set(cacheKey, data)
    return data
  }

  async getUrbanData(year: number, region: string = 'nepal_himalayas'): Promise<UrbanData> {
    const cacheKey = `urban_${year}_${region}`
    const cachedData = this.cache.get(cacheKey)
    
    if (cachedData) {
      return cachedData
    }
    
    const data = await this.client.getUrbanData(year, region)
    this.cache.set(cacheKey, data)
    return data
  }

  async getTemperatureData(year: number, region: string = 'nepal_himalayas'): Promise<TemperatureData> {
    const cacheKey = `temperature_${year}_${region}`
    const cachedData = this.cache.get(cacheKey)
    
    if (cachedData) {
      return cachedData
    }
    
    const data = await this.client.getTemperatureData(year, region)
    this.cache.set(cacheKey, data)
    return data
  }

  async getEnvironmentalSummary(year: number, region: string = 'nepal_himalayas'): Promise<EnvironmentalSummary> {
    const cacheKey = `summary_${year}_${region}`
    const cachedData = this.cache.get(cacheKey)
    
    if (cachedData) {
      return cachedData
    }
    
    const data = await this.client.getEnvironmentalSummary(year, region)
    this.cache.set(cacheKey, data)
    return data
  }

  // Non-cached methods for dynamic data
  async getRegions(): Promise<RegionInfo[]> {
    return this.client.getRegions().then(result => result.regions)
  }

  async generateReport(request: ReportRequest): Promise<any> {
    return this.client.generateReport(request)
  }

  async exportData(request: ExportRequest): Promise<any> {
    return this.client.exportData(request)
  }

  // Cache management
  clearCache(): void {
    this.cache.clear()
  }

  getCacheStatus(): { size: number; keys: string[] } {
    return {
      size: this.cache['cache'].size,
      keys: Array.from(this.cache['cache'].keys())
    }
  }
}

// Global API service instance
export const apiService = new EOApiService()

// Export client directly for specific use cases
export const apiClient = new EOApiClient()

// API status and configuration
export const apiConfig = {
  baseURL: API_BASE_URL,
  version: API_VERSION,
  timeout: API_TIMEOUT,
  endpoints: {
    environmental: '/environmental',
    maps: '/maps',
    reports: '/reports',
    health: '/health'
  }
}
