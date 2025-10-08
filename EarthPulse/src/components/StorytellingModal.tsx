import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  FaTimes, 
  FaArrowLeft, 
  FaArrowRight, 
  FaPlay, 
  FaPause,
  FaInfoCircle,
  FaExclamationTriangle,
  FaChartLine,
  FaUsers,
  FaGlobe
} from 'react-icons/fa'

interface StorytellingModalProps {
  onClose: () => void
  currentYear: number
  selectedIndicator: string
}

const StorytellingModal: React.FC<StorytellingModalProps> = ({
  onClose,
  currentYear
}) => {
  const [currentStory, setCurrentStory] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [imageError, setImageError] = useState(false)

  const stories = [
    {
      id: 'glacier-retreat',
      title: 'The Vanishing Glaciers',
      subtitle: 'Himalayan Glacier Retreat 2000-2025',
      image: '/api/placeholder/600/400',
      content: {
        problem: 'Glaciers in the Himalayas have retreated by an average of 15-20% over the past two decades, with some losing up to 30% of their mass.',
        impact: 'This affects water availability for over 1.6 billion people who depend on rivers fed by these glaciers.',
        data: {
          glacierLoss: '31%',
          affectedPeople: '1.6B',
          temperatureRise: '+2.2°C'
        },
        callToAction: 'Understanding glacier retreat helps us prepare for future water challenges and climate adaptation.'
      }
    },
    {
      id: 'urban-expansion',
      title: 'The Growing Cities',
      subtitle: 'Urban Growth in Kathmandu Valley',
      image: '/api/placeholder/600/400',
      content: {
        problem: 'Kathmandu Valley has experienced rapid urban expansion, with built-up areas increasing by 275% since 2000.',
        impact: 'This rapid growth has led to loss of agricultural land, increased pollution, and strain on infrastructure.',
        data: {
          urbanGrowth: '275%',
          populationGrowth: '180%',
          agriculturalLoss: '42%'
        },
        callToAction: 'Sustainable urban planning is crucial for managing growth while preserving environmental quality.'
      }
    },
    {
      id: 'temperature-rise',
      title: 'A Warming World',
      subtitle: 'Temperature Changes in the Region',
      image: '/api/placeholder/600/400',
      content: {
        problem: 'Average temperatures have risen by 1.8°C in the region over the past 25 years, with high-altitude areas warming even faster.',
        impact: 'This warming affects agriculture, water resources, and increases the risk of extreme weather events.',
        data: {
          temperatureRise: '+1.8°C',
          extremeEvents: '+40%',
          cropYield: '-15%'
        },
        callToAction: 'Climate adaptation strategies are essential for protecting communities and ecosystems.'
      }
    },
    {
      id: 'vegetation-changes',
      title: 'Changing Landscapes',
      subtitle: 'Vegetation and Forest Cover Changes',
      image: '/api/placeholder/600/400',
      content: {
        problem: 'Vegetation health has declined in many areas, with NDVI values dropping by 29% in some regions due to deforestation and climate stress.',
        impact: 'This affects biodiversity, carbon storage, and the livelihoods of communities dependent on forest resources.',
        data: {
          vegetationDecline: '29%',
          forestLoss: '18%',
          carbonStorage: '-25%'
        },
        callToAction: 'Protecting and restoring vegetation is key to climate mitigation and ecosystem health.'
      }
    }
  ]

  const handleNext = () => {
    setCurrentStory((prev) => (prev + 1) % stories.length)
  }

  const handlePrevious = () => {
    setCurrentStory((prev) => (prev - 1 + stories.length) % stories.length)
  }

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying)
  }

  const currentStoryData = stories[currentStory]

  return (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
      >
        <motion.div
          className="bg-space-dark border border-blue-400/30 rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden"
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.8, opacity: 0 }}
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-blue-500/20">
            <div>
              <h2 className="text-2xl font-nasa font-bold text-white">
                {currentStoryData.title}
              </h2>
              <p className="text-blue-300 text-sm">
                {currentStoryData.subtitle}
              </p>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <button
                  onClick={handlePrevious}
                  className="p-2 bg-blue-600/20 hover:bg-blue-600/40 border border-blue-400/30 rounded-lg text-blue-400 transition-all duration-300"
                >
                  <FaArrowLeft className="w-4 h-4" />
                </button>
                
                <button
                  onClick={handlePlayPause}
                  className="p-2 bg-green-600/20 hover:bg-green-600/40 border border-green-400/30 rounded-lg text-green-400 transition-all duration-300"
                >
                  {isPlaying ? <FaPause className="w-4 h-4" /> : <FaPlay className="w-4 h-4" />}
                </button>
                
                <button
                  onClick={handleNext}
                  className="p-2 bg-blue-600/20 hover:bg-blue-600/40 border border-blue-400/30 rounded-lg text-blue-400 transition-all duration-300"
                >
                  <FaArrowRight className="w-4 h-4" />
                </button>
              </div>
              
              <button
                onClick={onClose}
                className="p-2 bg-red-600/20 hover:bg-red-600/40 border border-red-400/30 rounded-lg text-red-400 transition-all duration-300"
              >
                <FaTimes className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="flex flex-col md:flex-row h-[70vh] md:h-[60vh]">
            {/* Left Side - Image/Visualization */}
            <div className="w-full md:w-1/2 p-4 md:p-6">
              <div className="h-full bg-gradient-to-br from-blue-900/20 to-purple-900/20 rounded-xl border border-blue-400/20 flex items-center justify-center relative overflow-hidden">
                {/* Satellite imagery */}
                <img
                  src={`${(import.meta.env.VITE_API_BASE_URL || (typeof window !== 'undefined' ? `${window.location.protocol}//${window.location.hostname}:8000` : 'http://localhost:8000'))}/api/v1/maps/gibs/snapshot?layer=MODIS_Terra_NDVI_16Day&year=${currentYear}&month=6&day=15&width=600&height=400&bbox=26,80,30.5,88.5`}
                  alt={currentStoryData.title}
                  className="max-h-full max-w-full object-cover rounded relative z-10"
                  onError={() => setImageError(true)}
                />
                
                {/* Fallback icon if image fails */}
                {imageError && (
                  <div className="absolute inset-0 flex items-center justify-center pointer-events-none z-0">
                    <FaGlobe className="text-6xl text-blue-400 opacity-30" />
                  </div>
                )}
                
                {/* Data overlay */}
                <div className="absolute top-4 left-4 bg-black/60 backdrop-blur-sm rounded-lg p-3">
                  <div className="text-white text-sm font-bold">
                    {currentYear} Data
                  </div>
                  <div className="text-blue-300 text-xs">
                    NASA Earth Observation
                  </div>
                </div>
              </div>
            </div>

            {/* Right Side - Story Content */}
            <div className="w-full md:w-1/2 p-4 md:p-6 overflow-y-auto">
              <div className="space-y-6">
                {/* Problem Statement */}
                <div className="bg-red-600/10 border border-red-400/30 rounded-lg p-4">
                  <div className="flex items-center space-x-2 mb-2">
                    <FaExclamationTriangle className="text-red-400 w-5 h-5" />
                    <h3 className="text-red-400 font-bold">The Challenge</h3>
                  </div>
                  <p className="text-white text-sm leading-relaxed">
                    {currentStoryData.content.problem}
                  </p>
                </div>

                {/* Impact */}
                <div className="bg-blue-600/10 border border-blue-400/30 rounded-lg p-4">
                  <div className="flex items-center space-x-2 mb-2">
                    <FaUsers className="text-blue-400 w-5 h-5" />
                    <h3 className="text-blue-400 font-bold">Human Impact</h3>
                  </div>
                  <p className="text-white text-sm leading-relaxed">
                    {currentStoryData.content.impact}
                  </p>
                </div>

                {/* Key Data */}
                <div className="bg-green-600/10 border border-green-400/30 rounded-lg p-4">
                  <div className="flex items-center space-x-2 mb-3">
                    <FaChartLine className="text-green-400 w-5 h-5" />
                    <h3 className="text-green-400 font-bold">Key Statistics</h3>
                  </div>
                  <div className="grid grid-cols-1 gap-3">
                    {Object.entries(currentStoryData.content.data).map(([key, value]) => (
                      <div key={key} className="flex justify-between items-center">
                        <span className="text-gray-300 text-sm capitalize">
                          {key.replace(/([A-Z])/g, ' $1').trim()}
                        </span>
                        <span className="text-white font-bold">
                          {value}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Call to Action */}
                <div className="bg-purple-600/10 border border-purple-400/30 rounded-lg p-4">
                  <div className="flex items-center space-x-2 mb-2">
                    <FaInfoCircle className="text-purple-400 w-5 h-5" />
                    <h3 className="text-purple-400 font-bold">Why This Matters</h3>
                  </div>
                  <p className="text-white text-sm leading-relaxed">
                    {currentStoryData.content.callToAction}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="p-6 border-t border-blue-500/20">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="text-sm text-gray-400">
                  Story {currentStory + 1} of {stories.length}
                </div>
                <div className="flex space-x-1">
                  {stories.map((_, index) => (
                    <button
                      key={index}
                      onClick={() => setCurrentStory(index)}
                      className={`w-2 h-2 rounded-full transition-all duration-300 ${
                        index === currentStory ? 'bg-blue-400' : 'bg-gray-600'
                      }`}
                    />
                  ))}
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-400">Share this story:</span>
                <button className="p-2 bg-blue-600/20 hover:bg-blue-600/40 border border-blue-400/30 rounded-lg text-blue-400 transition-all duration-300">
                  <FaChartLine className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  )
}

export default StorytellingModal
