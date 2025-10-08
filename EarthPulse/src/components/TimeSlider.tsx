import React from 'react'
import { motion } from 'framer-motion'

interface TimeSliderProps {
  currentYear: number
  onYearChange: (year: number) => void
}

const TimeSlider: React.FC<TimeSliderProps> = ({ currentYear, onYearChange }) => {
  const [isPlaying, setIsPlaying] = React.useState(false)

  const minYear = 2000
  const maxYear = 2025

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying)
  }

  // Simple range input instead of react-slider
  const handleSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onYearChange(parseInt(e.target.value))
  }

  return (
    <motion.div 
      className="bg-black/60 backdrop-blur-md border border-blue-400/30 rounded-2xl p-6 shadow-2xl"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, ease: "easeOut" }}
    >
      <div className="flex items-center space-x-6">
        {/* Play/Pause Button */}
        <div className="flex items-center space-x-2">
          <motion.button
            onClick={handlePlayPause}
            className="p-3 bg-blue-600/30 hover:bg-blue-600/50 border border-blue-400/50 rounded-lg text-blue-300 transition-all duration-300"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
          >
            {isPlaying ? '❚❚' : '▶'}
          </motion.button>
        </div>

        {/* Time Slider */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-blue-300 font-nasa">{minYear}</span>
            <span className="text-lg text-white font-nasa font-bold">{currentYear}</span>
            <span className="text-sm text-blue-300 font-nasa">{maxYear}</span>
          </div>
          
          <div className="relative">
            <input
              type="range"
              min={minYear}
              max={maxYear}
              value={currentYear}
              onChange={handleSliderChange}
              className="w-full h-2 bg-gradient-to-r from-green-500 via-blue-500 to-red-500 rounded-lg cursor-pointer appearance-none slider"
              style={{
                background: `linear-gradient(to right, 
                  #10b981 0%, 
                  #10b981 ${((currentYear - minYear) / (maxYear - minYear)) * 100}%, 
                  #374151 ${((currentYear - minYear) / (maxYear - minYear)) * 100}%, 
                  #374151 100%)`
              }}
            />
          </div>
        </div>
      </div>

      {/* Timeline Indicators */}
      <div className="mt-4 flex justify-between text-xs text-gray-400">
        <span>2000s - Early Data</span>
        <span>2010s - Modern Era</span>
        <span>2020s - Current</span>
      </div>
    </motion.div>
  )
}

export default TimeSlider