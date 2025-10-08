import React from 'react'
import { motion } from 'framer-motion'

const LoadingScreen: React.FC = () => {
  return (
    <div className="h-screen w-screen bg-space-dark flex items-center justify-center relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 bg-space-gradient">
        <div className="absolute inset-0 opacity-30" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='1'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
        }}></div>
      </div>

      {/* Floating Earth */}
      <motion.div
        className="relative z-10"
        animate={{ 
          rotate: 360,
          scale: [1, 1.1, 1]
        }}
        transition={{ 
          rotate: { duration: 20, repeat: Infinity, ease: "linear" },
          scale: { duration: 4, repeat: Infinity, ease: "easeInOut" }
        }}
      >
        <div className="w-32 h-32 bg-gradient-to-br from-blue-400 via-green-400 to-blue-600 rounded-full shadow-2xl relative overflow-hidden">
          {/* Earth continents */}
          <div className="absolute inset-0 opacity-60" style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M20 30 Q30 20 40 30 Q50 25 60 30 Q70 20 80 30 L80 70 Q70 60 60 70 Q50 75 40 70 Q30 80 20 70 Z' fill='%2310b981' opacity='0.8'/%3E%3C/svg%3E")`
          }}></div>
          
          {/* Glow effect */}
          <div className="absolute inset-0 rounded-full bg-gradient-to-br from-blue-400/20 to-transparent animate-pulse-glow"></div>
        </div>
      </motion.div>

      {/* Loading Text */}
      <motion.div
        className="absolute bottom-1/4 left-1/2 transform -translate-x-1/2 text-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1, duration: 1 }}
      >
        <h2 className="text-2xl font-nasa font-bold text-white mb-2">
          Earth Observation Visualizer
        </h2>
        <p className="text-blue-300 text-sm">
          Loading NASA satellite data...
        </p>
        
        {/* Loading dots */}
        <div className="flex justify-center mt-4 space-x-2">
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              className="w-2 h-2 bg-blue-400 rounded-full"
              animate={{ 
                scale: [1, 1.5, 1],
                opacity: [0.5, 1, 0.5]
              }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                delay: i * 0.2
              }}
            />
          ))}
        </div>
      </motion.div>

      {/* Satellite animation */}
      <motion.div
        className="absolute top-1/4 right-1/4 w-4 h-4 bg-white rounded-full"
        animate={{
          x: [0, 100, 0],
          y: [0, -50, 0],
          rotate: [0, 180, 360]
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      >
        <div className="w-full h-full bg-gradient-to-r from-blue-400 to-purple-400 rounded-full animate-pulse"></div>
      </motion.div>
    </div>
  )
}

export default LoadingScreen
