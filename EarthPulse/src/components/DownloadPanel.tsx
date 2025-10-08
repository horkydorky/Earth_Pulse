import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  FaTimes, 
  FaDownload, 
  FaFilePdf, 
  FaFileImage, 
  FaFileCsv,
  FaCheck,
  FaSpinner
} from 'react-icons/fa'
import { apiService, apiConfig } from '../services/api'

interface DownloadPanelProps {
  onClose: () => void
  currentYear: number
  selectedIndicator: string
}

const DownloadPanel: React.FC<DownloadPanelProps> = ({
  onClose,
  currentYear,
  selectedIndicator
}) => {
  const [selectedFormat, setSelectedFormat] = useState('pdf')
  const [selectedData, setSelectedData] = useState<string[]>(['map', 'charts', 'data'])
  const [isGenerating, setIsGenerating] = useState(false)
  const [isComplete, setIsComplete] = useState(false)
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null)
  const [downloadName, setDownloadName] = useState<string>('export')

  const formats = [
    {
      id: 'pdf',
      name: 'PDF Report',
      icon: FaFilePdf,
      description: 'Complete report with maps, charts, and analysis',
      color: 'red'
    },
    {
      id: 'image',
      name: 'Image Snapshot',
      icon: FaFileImage,
      description: 'High-resolution map and data visualization',
      color: 'blue'
    },
    {
      id: 'csv',
      name: 'Data Export',
      icon: FaFileCsv,
      description: 'Raw data for further analysis',
      color: 'green'
    }
  ]

  const dataOptions = [
    { id: 'map', name: 'Map Visualization', description: 'Current map view with all layers' },
    { id: 'charts', name: 'Data Charts', description: 'Environmental indicator charts' },
    { id: 'data', name: 'Raw Data', description: 'Numerical data for selected indicators' },
    { id: 'comparison', name: 'Comparison Data', description: 'Historical comparison data' },
    { id: 'metadata', name: 'Metadata', description: 'Data sources and methodology' }
  ]

  const handleGenerate = async () => {
    setIsGenerating(true)
    setIsComplete(false)
    setDownloadUrl(null)
    try {
      if (selectedFormat === 'pdf') {
        // Generate report on backend and capture download URL
        const report = await apiService.generateReport({
          report_type: 'comprehensive',
          year: currentYear,
          region: 'nepal_himalayas',
          indicators: ['ndvi','glacier','urban','temperature'],
          include_charts: selectedData.includes('charts'),
          include_maps: selectedData.includes('map')
        })
        const url = `${apiConfig.baseURL}/api/${apiConfig.version}${report.download_url}`
        setDownloadUrl(url)
        setDownloadName(`earth-observation-${currentYear}-${selectedIndicator}.pdf`)
        setIsComplete(true)
      } else if (selectedFormat === 'csv' || selectedFormat === 'json') {
        // Export data and prepare a blob URL for download
        const endpoint = `${apiConfig.baseURL}/api/${apiConfig.version}/reports/export`
        const body = {
          format: selectedFormat,
          indicators: ['ndvi','glacier','urban','temperature'],
          region: 'nepal_himalayas',
          start_year: 2000,
          end_year: currentYear,
          include_raw_data: selectedData.includes('data')
        }
        const resp = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': selectedFormat === 'csv' ? 'text/csv' : 'application/json' },
          body: JSON.stringify(body)
        })
        if (!resp.ok) throw new Error(`Export failed: ${resp.status}`)
        const blob = await resp.blob()
        const url = URL.createObjectURL(blob)
        setDownloadUrl(url)
        setDownloadName(`environmental_data_${currentYear}.${selectedFormat}`)
        setIsComplete(true)
      } else {
        // Image snapshot placeholder – use map/story capture later
        setIsComplete(false)
      }
    } catch (e) {
      console.error('Export/Report failed:', e)
      setIsComplete(false)
    } finally {
      setIsGenerating(false)
    }
  }

  const handleDownload = () => {
    if (!downloadUrl) return
    const link = document.createElement('a')
    link.href = downloadUrl
    link.download = downloadName
    link.target = '_blank'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <motion.div
      className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={onClose}
    >
      <motion.div
        className="bg-space-dark border border-blue-400/30 rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden"
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.8, opacity: 0 }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-blue-500/20">
          <div>
            <h2 className="text-2xl font-nasa font-bold text-white">
              Export Data
            </h2>
            <p className="text-blue-300 text-sm">
              Generate reports and download data for {currentYear}
            </p>
          </div>
          
          <button
            onClick={onClose}
            className="p-2 bg-red-600/20 hover:bg-red-600/40 border border-red-400/30 rounded-lg text-red-400 transition-all duration-300"
          >
            <FaTimes className="w-4 h-4" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6 overflow-y-auto max-h-[60vh]">
          {/* Format Selection */}
          <div>
            <h3 className="text-lg font-bold text-white mb-4">Export Format</h3>
            <div className="grid grid-cols-1 gap-3">
              {formats.map((format) => {
                const Icon = format.icon
                return (
                  <motion.button
                    key={format.id}
                    onClick={() => setSelectedFormat(format.id)}
                    className={`p-4 rounded-lg border transition-all duration-300 text-left ${
                      selectedFormat === format.id
                        ? `border-${format.color}-400/50 bg-${format.color}-600/20`
                        : 'border-gray-600/30 hover:border-blue-400/30'
                    }`}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <div className="flex items-center space-x-3">
                      <Icon className={`text-${format.color}-400 w-6 h-6`} />
                      <div>
                        <div className="text-white font-medium">
                          {format.name}
                        </div>
                        <div className="text-gray-400 text-sm">
                          {format.description}
                        </div>
                      </div>
                    </div>
                  </motion.button>
                )
              })}
            </div>
          </div>

          {/* Data Selection */}
          <div>
            <h3 className="text-lg font-bold text-white mb-4">Include Data</h3>
            <div className="space-y-2">
              {dataOptions.map((option) => (
                <motion.label
                  key={option.id}
                  className="flex items-center space-x-3 p-3 bg-black/30 rounded-lg border border-gray-600/30 hover:border-blue-400/30 transition-all duration-300 cursor-pointer"
                  whileHover={{ scale: 1.01 }}
                >
                  <input
                    type="checkbox"
                    checked={selectedData.includes(option.id)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedData([...selectedData, option.id])
                      } else {
                        setSelectedData(selectedData.filter(id => id !== option.id))
                      }
                    }}
                    className="w-4 h-4 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500"
                  />
                  <div>
                    <div className="text-white text-sm font-medium">
                      {option.name}
                    </div>
                    <div className="text-gray-400 text-xs">
                      {option.description}
                    </div>
                  </div>
                </motion.label>
              ))}
            </div>
          </div>

          {/* Export Settings */}
          <div>
            <h3 className="text-lg font-bold text-white mb-4">Export Settings</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-black/30 rounded-lg border border-gray-600/30">
                <span className="text-white text-sm">Resolution</span>
                <select className="bg-gray-700 text-white text-sm rounded px-3 py-1 border border-gray-600">
                  <option>High (300 DPI)</option>
                  <option>Medium (150 DPI)</option>
                  <option>Low (72 DPI)</option>
                </select>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-black/30 rounded-lg border border-gray-600/30">
                <span className="text-white text-sm">Time Range</span>
                <select className="bg-gray-700 text-white text-sm rounded px-3 py-1 border border-gray-600">
                  <option>Current Year Only</option>
                  <option>Last 5 Years</option>
                  <option>Full Dataset (2000-2025)</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-blue-500/20">
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-400">
              Selected: {selectedData.length} data types • {formats.find(f => f.id === selectedFormat)?.name}
            </div>
            
            <div className="flex items-center space-x-3">
              {isComplete ? (
                <motion.div
                  className="flex items-center space-x-2 text-green-400"
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                >
                  <FaCheck className="w-4 h-4" />
                  <span className="text-sm font-medium">Ready!</span>
                </motion.div>
              ) : (
                <motion.button
                  onClick={handleGenerate}
                  disabled={isGenerating}
                  className="flex items-center space-x-2 px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white rounded-lg transition-all duration-300"
                  whileHover={{ scale: isGenerating ? 1 : 1.05 }}
                  whileTap={{ scale: isGenerating ? 1 : 0.95 }}
                >
                  {isGenerating ? (
                    <>
                      <FaSpinner className="w-4 h-4 animate-spin" />
                      <span>Generating...</span>
                    </>
                  ) : (
                    <>
                      <FaDownload className="w-4 h-4" />
                      <span>Generate</span>
                    </>
                  )}
                </motion.button>
              )}
              
              {isComplete && downloadUrl && (
                <motion.button
                  onClick={handleDownload}
                  className="flex items-center space-x-2 px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-all duration-300"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <FaDownload className="w-4 h-4" />
                  <span>Download</span>
                </motion.button>
              )}
            </div>
          </div>
        </div>
      </motion.div>
    </motion.div>
  )
}

export default DownloadPanel
