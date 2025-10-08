import React, { useEffect, useState } from 'react'
import { MapContainer as LeafletMap, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import L from 'leaflet'
import { motion } from 'framer-motion'
import { apiService, EnvironmentalDataPoint } from '../services/api'

// Fix for default markers in React Leaflet
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

interface MapContainerProps {
  currentYear: number
  selectedIndicator: string
}

interface MapDataPoint {
  id: string
  position: [number, number]
  title: string
  description: string
  type: string
  value: number
  confidence?: number
}

// Custom hook to update map when year changes
const MapUpdater: React.FC<{ year: number; indicator: string }> = ({ year, indicator }) => {
  const map = useMap()
  
  useEffect(() => {
    console.log(`Updating map for year ${year} with indicator ${indicator}`)
  }, [year, indicator, map])

  return null
}

const MapContainer: React.FC<MapContainerProps> = ({ currentYear, selectedIndicator }) => {
  const [mapCenter] = useState<[number, number]>([27.7172, 85.3240]) // Kathmandu, Nepal
  const [mapZoom] = useState(8)
  const [isLoading, setIsLoading] = useState(false)
  const [mapDataPoints, setMapDataPoints] = useState<MapDataPoint[]>([])
  const [error, setError] = useState<string | null>(null)

  // Fetch environmental data when year or indicator changes
  useEffect(() => {
    const fetchEnvironmentalData = async () => {
      setIsLoading(true)
      setError(null)
      
      try {
        let environmentalData
        
        switch (selectedIndicator) {
          case 'ndvi':
            environmentalData = await apiService.getNDVIData(currentYear, 'nepal_himalayas')
            break
          case 'glacier':
            environmentalData = await apiService.getGlacierData(currentYear, 'nepal_himalayas')
            break
          case 'urban':
            environmentalData = await apiService.getUrbanData(currentYear, 'nepal_himalayas')
            break
          case 'temperature':
            environmentalData = await apiService.getTemperatureData(currentYear, 'nepal_himalayas')
            break
          default:
            // Get summary data
            environmentalData = await apiService.getEnvironmentalSummary(currentYear, 'nepal_himalayas')
            break
        }

        // Transform environmental data to map points
        await transformEnvironmentalDataToMapPoints(environmentalData, selectedIndicator)
        
      } catch (err) {
        console.error('Failed to fetch environmental data:', err)
        setError('Failed to load environmental data. Using sample data.')
        
        // Fallback to sample data
        generateSampleMapPoints()
      } finally {
        setIsLoading(false)
      }
    }

    fetchEnvironmentalData()
  }, [currentYear, selectedIndicator])

  const transformEnvironmentalDataToMapPoints = async (data: any, indicator: string) => {
    let dataPoints: EnvironmentalDataPoint[] = []
    
    if (indicator === 'ndvi' && data.data_points) {
      dataPoints = data.data_points
    } else if (indicator === 'glacier' && data.data_points) {
      dataPoints = data.data_points
    } else if (indicator === 'urban' && data.data_points) {
      dataPoints = data.data_points
    } else if (indicator === 'temperature' && data.data_points) {
      dataPoints = data.data_points
    }

    // Convert environmental data points to map markers
    const mapPoints: MapDataPoint[] = dataPoints.map((point: EnvironmentalDataPoint, index: number) => ({
      id: `${indicator}_${index}`,
      position: [point.latitude, point.longitude] as [number, number],
      title: getIndicatorTitle(indicator),
      description: generateDescription(indicator, point.value, currentYear),
      type: indicator,
      value: point.value,
      confidence: point.confidence
    }))

    setMapDataPoints(mapPoints)
  }

  const generateSampleMapPoints = () => {
    // Sample data points for demonstration when API fails
    const samplePoints: MapDataPoint[] = [
      {
        id: 'sample_1',
        position: [27.7172, 85.3240] as [number, number],
        title: 'Kathmandu Valley',
        description: `${getIndicatorTitle(selectedIndicator)} analysis for ${currentYear}`,
        type: selectedIndicator,
        value: getSampleValue(selectedIndicator)
      },
      {
        id: 'sample_2',
        position: [28.3949, 84.1240] as [number, number],
        title: 'Annapurna Region',
        description: `${selectedIndicator} data collected for ${currentYear}`,
        type: selectedIndicator,
        value: getSampleValue(selectedIndicator)
      },
      {
        id: 'sample_3',
        position: [27.9881, 86.9250] as [number, number],
        title: 'Everest Region',
        description: `Environmental monitoring point for ${selectedIndicator}`,
        type: selectedIndicator,
        value: getSampleValue(selectedIndicator)
      }
    ]
    setMapDataPoints(samplePoints)
  }

  const getIndicatorTitle = (indicator: string): string => {
    const titles = {
      ndvi: 'Vegetation Index (NDVI)',
      glacier: 'Glacier Coverage',
      urban: 'Urban Expansion',
      temperature: 'Surface Temperature'
    }
    return titles[indicator as keyof typeof titles] || indicator.toUpperCase()
  }

  const generateDescription = (indicator: string, value: number, year: number): string => {
    switch (indicator) {
      case 'ndvi':
        return `Vegetation health: ${value.toFixed(3)} NDVI in ${year}`
      case 'glacier':
        return `Glacier area: ${value.toFixed(1)} km² in ${year}`
      case 'urban':
        return `Urban coverage: ${value.toFixed(1)} km² in ${year}`
      case 'temperature':
        return `Temperature: ${value.toFixed(1)}°C in ${year}`
      default:
        return `${indicator} measurement: ${value.toFixed(2)} in ${year}`
    }
  }

  const getSampleValue = (indicator: string): number => {
    const sampleValues = {
      ndvi: 0.65,
      glacier: 1250.0,
      urban: 450.0,
      temperature: 18.5
    }
    return sampleValues[indicator as keyof typeof sampleValues] || 0
  }

  const getMarkerIcon = (type: string, value?: number) => {
    const colors = {
      urban: '#f59e0b',
      glacier: '#0ea5e9',
      temperature: '#ef4444',
      ndvi: '#10b981',
      vegetation: '#10b981'
    }

    const color = colors[type as keyof typeof colors] || '#0ea5e9'
    const size = value ? Math.min(Math.max(value * 2, 15), 30) : 20

    return L.divIcon({
      className: 'custom-marker',
      html: `<div style="
        width: ${size}px; 
        height: ${size}px; 
        background: ${color}; 
        border: 2px solid white; 
        border-radius: 50%; 
        box-shadow: 0 0 10px ${color};
      "></div>`,
      iconSize: [size, size],
      iconAnchor: [size/2, size/2]
    })
  }

  return (
    <div className="relative h-full w-full">
      {/* Error Message */}
      {error && (
        <motion.div 
          className="absolute top-4 left-1/2 transform -translate-x-1/2 z-30 bg-red-600/20 backdrop-blur-sm border border-red-400/30 rounded-lg px-4 py-2"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="text-red-400 text-sm">
            ⚠️ {error}
          </div>
        </motion.div>
      )}

      {/* Loading Overlay */}
      {isLoading && (
        <motion.div 
          className="absolute inset-0 bg-black/50 backdrop-blur-sm z-20 flex items-center justify-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <div className="text-center">
            <div className="w-8 h-8 border-2 border-blue-400 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
            <p className="text-white text-sm">Loading {selectedIndicator} data for {currentYear}...</p>
            <p className="text-gray-400 text-xs">Fetching from NASA EO API</p>
          </div>
        </motion.div>
      )}

      {/* Map */}
      <LeafletMap
        center={mapCenter}
        zoom={mapZoom}
        style={{ height: '100%', width: '100%' }}
        className="z-10"
      >
        {/* Custom Dark Tile Layer with API integration */}
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        />
        
        {/* Map Updater */}
        <MapUpdater year={currentYear} indicator={selectedIndicator} />
        
        {/* Dynamic Data Points */}
        {mapDataPoints.map((point) => (
          <Marker
            key={point.id}
            position={point.position}
            icon={getMarkerIcon(point.type, point.value)}
          >
            <Popup className="custom-popup">
              <div className="p-3 min-w-[200px]">
                <h3 className="font-bold text-gray-800 mb-2">{point.title}</h3>
                <p className="text-sm text-gray-600 mb-3">{point.description}</p>
                <div className="space-y-2">
                  <div className="text-xs text-gray-500">
                    Value: {point.value.toFixed(2)}
                    {point.confidence && ` (Confidence: ${Math.round(point.confidence * 100)}%)`}
                  </div>
                  <div className="flex space-x-2">
                    <button className="px-3 py-1 bg-blue-500 text-white text-xs rounded hover:bg-blue-600 transition-colors">
                      View Details
                    </button>
                    <button className="px-3 py-1 bg-green-500 text-white text-xs rounded hover:bg-green-600 transition-colors">
                      Compare Years
                    </button>
                  </div>
                </div>
              </div>
            </Popup>
          </Marker>
        ))}
      </LeafletMap>

      {/* Enhanced Map Controls */}
      <div className="absolute top-4 right-4 z-20 space-y-2">
        <motion.button
          className="p-2 bg-black/50 backdrop-blur-sm border border-blue-400/30 rounded-lg text-white hover:bg-blue-600/30 transition-all duration-300"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          title="Refresh Data"
        >
          🔄
        </motion.button>
        
        <motion.button
          className="p-2 bg-black/50 backdrop-blur-sm border border-green-400/30 rounded-lg text-white hover:bg-green-600/30 transition-all duration-300"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          title="API Status"
        >
          📡
        </motion.button>
      </div>

      {/* Enhanced Year Display */}
      <motion.div 
        className="absolute top-4 left-4 z-20 bg-black/50 backdrop-blur-sm border border-blue-400/30 rounded-lg px-4 py-2"
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.5 }}
      >
        <div className="text-white text-sm font-nasa">
          <div className="text-blue-400">Current Year</div>
          <div className="text-2xl font-bold">{currentYear}</div>
        </div>
      </motion.div>

      {/* Enhanced Indicator Display */}
      <motion.div 
        className="absolute top-20 left-4 z-20 bg-black/50 backdrop-blur-sm border border-green-400/30 rounded-lg px-4 py-2"
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.7 }}
      >
        <div className="text-white text-sm font-nasa">
          <div className="text-green-400">Active Layer</div>
          <div className="text-lg font-bold">{getIndicatorTitle(selectedIndicator)}</div>
          <div className="text-xs text-gray-400">{mapDataPoints.length} data points</div>
        </div>
      </motion.div>

      {/* Data Source Info */}
      <motion.div 
        className="absolute bottom-4 right-4 z-20 bg-black/50 backdrop-blur-sm border border-gray-400/30 rounded-lg px-3 py-2"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1 }}
      >
        <div className="text-gray-400 text-xs">
          <div>Data Source: NASA EO API</div>
          <div>Real-time: {isLoading ? 'Loading...' : 'Live'}</div>
        </div>
      </motion.div>
    </div>
  )
}

export default MapContainer