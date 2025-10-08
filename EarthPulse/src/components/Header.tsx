import React from 'react'
import { motion } from 'framer-motion'
import { 
  FaSatellite, 
  FaChartLine, 
  FaBook, 
  FaDownload,
  FaGlobe,
  FaSignal,
  FaEye
} from 'react-icons/fa'

interface HeaderProps {
  onToggleComparison: () => void
  onToggleStory: () => void
  onToggleDownload: () => void
}

const Header: React.FC<HeaderProps> = ({ 
  onToggleComparison, 
  onToggleStory, 
  onToggleDownload 
}) => {
  return (
    <motion.header 
      className="absolute top-0 left-0 right-0 z-30 bg-black/30 backdrop-blur-md border-b border-blue-400/20"
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 1, ease: "easeOut" }}
    >
      <div className="flex items-center justify-between px-4 md:px-8 py-4 md:py-5">
        {/* Enhanced Logo and Title */}
        <motion.div 
          className="flex items-center space-x-4"
          whileHover={{ scale: 1.03 }}
        >
          <div className="relative group">
            {/* Floating Earth with glow */}
            <motion.div
              className="relative"
              animate={{ 
                rotateY: [0, 360],
              }}
              transition={{ 
                duration: 20, 
                repeat: Infinity, 
                ease: "linear" 
              }}
            >
              <FaGlobe className="text-4xl text-blue-400 group-hover:text-blue-300 transition-colors duration-300" />
            </motion.div>
            
            {/* Orbital satellite */}
            <motion.div
              className="absolute -top-2 -right-2 w-4 h-4"
              animate={{ 
                rotate: 360,
              }}
              transition={{ 
                duration: 8, 
                repeat: Infinity, 
                ease: "linear" 
              }}
            >
              <FaSatellite className="w-4 h-4 text-green-400" />
            </motion.div>

            {/* Status dot */}
            <motion.div
              className="absolute -bottom-1 -right-1 w-3 h-3 bg-green-400 rounded-full"
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            />
          </div>
          
          <div>
            <motion.h1 
              className="text-2xl font-nasa font-bold text-white"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
            >
              Earth Observer
            </motion.h1>
            <motion.div 
              className="flex items-center space-x-2"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.7 }}
            >
              <FaEye className="text-xs text-blue-300" />
              <span className="text-xs text-blue-300 font-medium">NASA DATA VISUALIZATION STUDIO</span>
            </motion.div>
          </div>
        </motion.div>

        {/* Enhanced Navigation Buttons */}
        <div className="flex items-center space-x-2 md:space-x-3">
          <motion.button
            onClick={onToggleComparison}
            className="group flex items-center space-x-2 md:space-x-3 px-4 md:px-6 py-2 md:py-3 bg-gradient-to-r from-blue-600/20 to-blue-500/20 hover:from-blue-600/40 hover:to-blue-500/40 border border-blue-400/40 rounded-xl transition-all duration-500 backdrop-blur-sm"
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.98 }}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            <FaChartLine className="text-blue-400 group-hover:text-blue-300 transition-colors duration-300 text-lg" />
            <span className="text-sm font-medium text-white group-hover:text-blue-100 transition-colors duration-300">
              Analysis
            </span>
          </motion.button>

          <motion.button
            onClick={onToggleStory}
            className="group flex items-center space-x-2 md:space-x-3 px-4 md:px-6 py-2 md:py-3 bg-gradient-to-r from-green-600/20 to-emerald-500/20 hover:from-green-600/40 hover:to-emerald-500/40 border border-green-400/40 rounded-xl transition-all duration-500 backdrop-blur-sm"
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.98 }}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
          >
            <FaBook className="text-green-400 group-hover:text-green-300 transition-colors duration-300 text-lg" />
            <span className="text-sm font-medium text-white group-hover:text-green-100 transition-colors duration-300">
              Stories
            </span>
          </motion.button>

          <motion.button
            onClick={onToggleDownload}
            className="group flex items-center space-x-2 md:space-x-3 px-4 md:px-6 py-2 md:py-3 bg-gradient-to-r from-purple-600/20 to-violet-500/20 hover:from-purple-600/40 hover:to-violet-500/40 border border-purple-400/40 rounded-xl transition-all duration-500 backdrop-blur-sm"
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.98 }}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
          >
            <FaDownload className="text-purple-400 group-hover:text-purple-300 transition-colors duration-300 text-lg" />
            <span className="text-sm font-medium text-white group-hover:text-purple-100 transition-colors duration-300">
              Export
            </span>
          </motion.button>

          {/* Enhanced Status Indicator */}
          <motion.div 
            className="flex items-center space-x-3 px-4 py-3 bg-gradient-to-r from-green-600/20 to-green-500/20 border border-green-400/40 rounded-xl backdrop-blur-sm"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: [1, 0.7, 1], scale: 1 }}
            transition={{ opacity: { duration: 3, repeat: Infinity }, scale: { duration: 0.6 } }}
          >
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            >
              <FaSignal className="text-green-400 w-4 h-4" />
            </motion.div>
            <div className="text-right">
              <div className="text-xs text-green-300 font-medium">REALTIME</div>
              <div className="text-xs text-green-400 font-bold">NASA FEED</div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Enhanced Progress Bar */}
      <motion.div 
        className="h-1 relative overflow-hidden"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
      >
        <div className="absolute inset-0 bg-gradient-to-r from-blue-500/20 via-purple-500/20 to-green-500/20"></div>
        <motion.div 
          className="h-full bg-gradient-to-r from-blue-500 via-green-500 to-purple-500"
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ duration: 3, ease: "easeOut", delay: 1 }}
          style={{ originX: 0 }}
        />
        <motion.div 
          className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-30"
          animate={{ translateX: ['-100%', '100%'] }}
          transition={{ duration: 3, repeat: Infinity, ease: "linear", delay: 1.5 }}
        />
      </motion.div>

      {/* Floating Particles */}
      <div className="absolute inset-0 pointer-events-none">
        {[...Array(6)].map((_, i) => (
          <motion.div
          key={i}
            className="absolute w-1 h-1 bg-blue-400/60 rounded-full"
            style={{
              left: `${20 + i * 15}%`,
              top: '50%',
            }}
            animate={{
              y: [-10, 10, -10],
              opacity: [0, 1, 0],
            }}
            transition={{
              duration: 3 + i * 0.5,
              repeat: Infinity,
              ease: "easeInOut",
              delay: i * 0.3,
            }}
          />
        ))}
      </div>
    </motion.header>
  )
}

export default Header
