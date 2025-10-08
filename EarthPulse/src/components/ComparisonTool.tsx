import React, { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { 
  FaExchangeAlt, 
  FaPlay, 
  FaDownload,
  FaChartBar,
  FaMapMarkerAlt
} from 'react-icons/fa'
import { apiService, ComparisonResult, NDVIData } from '../services/api'

interface ComparisonToolProps {
  currentYear: number
}

const ComparisonTool: React.FC<ComparisonToolProps> = ({ currentYear }) => {
  const [comparisonYear, setComparisonYear] = useState(2000)
  const [isAnimating, setIsAnimating] = useState(false)
  const [selectedRegion, setSelectedRegion] = useState('kathmandu')
  const [results, setResults] = useState<ComparisonResult[] | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const regions = [
    {
      id: 'kathmandu',
      name: 'Kathmandu Valley',
      coordinates: [27.7172, 85.3240],
      description: 'Urban expansion and development'
    },
    {
      id: 'annapurna',
      name: 'Annapurna Region',
      coordinates: [28.3949, 84.1240],
      description: 'Glacier retreat and mountain changes'
    },
    {
      id: 'everest',
      name: 'Everest Region',
      coordinates: [27.9881, 86.9250],
      description: 'High-altitude environmental changes'
    }
  ]

  // map UI region ids to backend region ids
  const regionIdMap: Record<string, string> = {
    kathmandu: 'kathmandu_valley',
    annapurna: 'annapurna_region',
    everest: 'everest_region'
  }

  // fetch comparison from backend (NDVI by default)
  useEffect(() => {
    const fetchComparison = async () => {
      setLoading(true)
      setError(null)
      try {
        const regionParam = regionIdMap[selectedRegion] || 'nepal_himalayas'
        const data = await apiService.getTemporalComparison(
          'ndvi',
          regionParam,
          comparisonYear,
          currentYear,
          false
        )
        setResults(data)
      } catch (e) {
        // Fallback: compute comparison on the client using two NDVI calls
        try {
          const regionParam = regionIdMap[selectedRegion] || 'nepal_himalayas'
          const baseline: NDVIData = await apiService.getNDVIData(comparisonYear, regionParam)
          const latest: NDVIData = await apiService.getNDVIData(currentYear, regionParam)
          const changeAmount = latest.average_ndvi - baseline.average_ndvi
          const changePct = baseline.average_ndvi !== 0 ? (changeAmount / baseline.average_ndvi) * 100 : 0
          const fallback: ComparisonResult = {
            comparison_type: 'temporal',
            region: regionParam,
            indicator: 'ndvi',
            baseline_year: comparisonYear,
            comparison_year: currentYear,
            baseline_value: Number(baseline.average_ndvi.toFixed(3)),
            comparison_value: Number(latest.average_ndvi.toFixed(3)),
            change_amount: Number(changeAmount.toFixed(3)),
            change_percentage: Number(changePct.toFixed(2)),
            trend_summary: `Vegetation health changed over ${currentYear - comparisonYear} years`,
            impact_assessment: 'Computed on client due to API fallback'
          }
          setResults([fallback])
        } catch (e2) {
          setError('Failed to load comparison')
          setResults(null)
        }
      } finally {
        setLoading(false)
      }
    }
    if (comparisonYear < currentYear) {
      fetchComparison()
    } else {
      setResults(null)
    }
  }, [comparisonYear, currentYear, selectedRegion])

  const handleSwapYears = () => {
    setIsAnimating(true)
    setTimeout(() => {
      // swap: set comparison year to an earlier baseline relative to current
      const baseline = Math.max(2000, Math.min(currentYear - 5, comparisonYear))
      setComparisonYear(baseline)
      setIsAnimating(false)
    }, 500)
  }

  const handleAnimateComparison = () => {
    setIsAnimating(true)
    setTimeout(() => setIsAnimating(false), 2000)
  }

  const currentData = results && results.length > 0 ? results[0] : null

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-blue-500/20">
        <h2 className="text-lg font-nasa font-bold text-white mb-2">
          Then vs Now
        </h2>
        <p className="text-sm text-blue-300">
          Compare environmental changes
        </p>
      </div>

      {/* Region Selector */}
      <div className="p-4 border-b border-blue-500/20">
        <h3 className="text-sm font-medium text-white mb-3">Select Region</h3>
        <div className="space-y-2">
          {regions.map((region) => (
            <motion.button
              key={region.id}
              onClick={() => setSelectedRegion(region.id)}
              className={`w-full text-left p-3 rounded-lg border transition-all duration-300 ${
                selectedRegion === region.id
                  ? 'border-blue-400/50 bg-blue-600/20'
                  : 'border-gray-600/30 hover:border-blue-400/30'
              }`}
              whileHover={{ scale: 1.02 }}
            >
              <div className="flex items-center space-x-3">
                <FaMapMarkerAlt className="text-blue-400 w-4 h-4" />
                <div>
                  <div className="text-white text-sm font-medium">
                    {region.name}
                  </div>
                  <div className="text-gray-400 text-xs">
                    {region.description}
                  </div>
                </div>
              </div>
            </motion.button>
          ))}
        </div>
      </div>

      {/* Year Comparison */}
      <div className="p-4 border-b border-blue-500/20">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-medium text-white">Time Comparison</h3>
          <motion.button
            onClick={handleSwapYears}
            className="p-2 bg-blue-600/20 hover:bg-blue-600/40 border border-blue-400/30 rounded-lg text-blue-400 transition-all duration-300"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
          >
            <FaExchangeAlt className="w-4 h-4" />
          </motion.button>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <motion.div
            className="text-center p-3 bg-green-600/20 border border-green-400/30 rounded-lg"
            animate={isAnimating ? { scale: [1, 1.05, 1] } : {}}
            transition={{ duration: 0.5 }}
          >
            <div className="text-green-400 text-xs font-medium mb-1">THEN</div>
            <div className="text-2xl font-bold text-white">{comparisonYear}</div>
          </motion.div>

          <motion.div
            className="text-center p-3 bg-blue-600/20 border border-blue-400/30 rounded-lg"
            animate={isAnimating ? { scale: [1, 1.05, 1] } : {}}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <div className="text-blue-400 text-xs font-medium mb-1">NOW</div>
            <div className="text-2xl font-bold text-white">{currentYear}</div>
          </motion.div>
        </div>
      </div>

      {/* Comparison Data */}
      <div className="flex-1 overflow-y-auto p-4">
        <h3 className="text-sm font-medium text-white mb-4">Change Analysis (NDVI)</h3>

        {loading && (
          <div className="text-xs text-gray-400">Loading comparison…</div>
        )}
        {error && (
          <div className="text-xs text-red-400">{error}</div>
        )}
        {!loading && !error && currentData && (
          <div className="space-y-4">
            <motion.div
              className="bg-black/30 backdrop-blur-sm border border-gray-600/30 rounded-lg p-4"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
            >
              <div className="flex items-center justify-between mb-2">
                <h4 className="text-white text-sm font-medium">Vegetation Index</h4>
                <div className={`text-xs font-medium ${currentData.change_amount >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {currentData.change_amount >= 0 ? '+' : ''}{currentData.change_percentage}%
                </div>
              </div>

              <div className="text-xs text-gray-400">
                {currentData.baseline_year}: {currentData.baseline_value} → {currentData.comparison_year}: {currentData.comparison_value}
              </div>

              <div className="mt-2 h-2 bg-gray-700 rounded-full overflow-hidden">
                <motion.div
                  className={`h-full ${currentData.change_amount >= 0 ? 'bg-green-500' : 'bg-red-500'}`}
                  initial={{ width: 0 }}
                  animate={{ width: `${Math.min(100, Math.abs(currentData.change_percentage))}%` }}
                />
              </div>

              <div className="mt-2 text-xs text-blue-300">{currentData.trend_summary}</div>
            </motion.div>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="p-4 border-t border-blue-500/20 space-y-2">
        <motion.button
          onClick={handleAnimateComparison}
          className="w-full flex items-center justify-center space-x-2 py-2 bg-blue-600/20 hover:bg-blue-600/40 border border-blue-400/30 rounded-lg text-blue-300 transition-all duration-300"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <FaPlay className="w-4 h-4" />
          <span className="text-sm font-medium">Animate Comparison</span>
        </motion.button>

        <motion.button
          className="w-full flex items-center justify-center space-x-2 py-2 bg-green-600/20 hover:bg-green-600/40 border border-green-400/30 rounded-lg text-green-300 transition-all duration-300"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <FaDownload className="w-4 h-4" />
          <span className="text-sm font-medium">Export Report</span>
        </motion.button>
      </div>
    </div>
  )
}

export default ComparisonTool
