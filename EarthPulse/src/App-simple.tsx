import { useState } from 'react'

function App() {
  const [currentYear, setCurrentYear] = useState(2020)

  return (
    <div className="h-screen w-screen bg-black text-white flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">🌍 Earth Observer</h1>
        <p className="text-xl mb-8">NASA Data Visualization Studio</p>
        <div className="space-y-4">
          <p>Current Year: {currentYear}</p>
          <input
            type="range"
            min="2000"
            max="2025"
            value={currentYear}
            onChange={(e) => setCurrentYear(parseInt(e.target.value))}
            className="w-64"
          />
          <p>Testing basic functionality...</p>
        </div>
      </div>
    </div>
  )
}

export default App
