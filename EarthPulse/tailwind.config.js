/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'space-dark': '#0a0a0a',
        'space-darker': '#050505',
        'space-blue': '#1e3a8a',
        'space-purple': '#7c3aed',
        'earth-green': '#10b981',
        'earth-deep': '#065f46',
        'glacier-blue': '#0ea5e9',
        'glacier-deep': '#0369a1',
        'urban-orange': '#f59e0b',
        'urban-deep': '#d97706',
        'temperature-red': '#ef4444',
        'temperature-deep': '#dc2626',
        'nasa-gold': '#fbbf24',
        'cosmic-purple': '#a855f7',
        'nebula-blue': '#3b82f6',
        'aurora-green': '#34d399'
      },
      fontFamily: {
        'nasa': ['Orbitron', 'monospace'],
        'sans': ['Inter', 'sans-serif'],
        'code': ['Fira Code', 'monospace']
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'float-delayed': 'float 6s ease-in-out infinite 2s',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'pulse-glow': 'pulse-glow 4s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'spin-slow': 'spin 3s linear infinite',
        'bounce-slow': 'bounce 3s infinite',
        'ping-slow': 'ping 4s cubic-bezier(0, 0, 0.2, 1) infinite',
        'wiggle': 'wiggle 1s ease-in-out infinite',
        'heartbeat': 'heartbeat 2s ease-in-out infinite',
        'orbit': 'orbit 20s linear infinite',
        'earth-spin': 'earth-spin 30s linear infinite',
        'satellite-orbit': 'satellite-orbit 15s linear infinite'
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' }
        },
        'pulse-glow': {
          '0%, 100%': { 
            opacity: '0.3',
            transform: 'scale(1)'
          },
          '50%': { 
            opacity: '0.6',
            transform: 'scale(1.2)'
          }
        },
        glow: {
          '0%': { 
            boxShadow: '0 0 5px #0ea5e9, 0 0 10px #0ea5e9, 0 0 15px #0ea5e9',
            textShadow: '0 0 5px #0ea5e9, 0 0 10px #0ea5e9, 0 0 15px #0ea5e9'
          },
          '100%': { 
            boxShadow: '0 0 10px #0ea5e9, 0 0 20px #0ea5e9, 0 0 30px #0ea5e9',
            textShadow: '0 0 10px #0ea5e9, 0 0 20px #0ea5e9, 0 0 30px #0ea5e9'
          }
        },
        wiggle: {
          '0%, 100%': { transform: 'rotate(-3deg)' },
          '50%': { transform: 'rotate(3deg)' }
        },
        heartbeat: {
          '0%, 100%': { transform: 'scale(1)' },
          '25%': { transform: 'scale(1.1)' },
          '50%': { transform: 'scale(1)' },
          '75%': { transform: 'scale(1.05)' }
        },
        orbit: {
          '0%': { transform: 'rotate(0deg) translateX(100px) rotate(0deg)' },
          '100%': { transform: 'rotate(360deg) translateX(100px) rotate(-360deg)' }
        },
        'earth-spin': {
          '0%': { transform: 'rotateY(0deg)' },
          '100%': { transform: 'rotateY(360deg)' }
        },
        'satellite-orbit': {
          '0%': { 
            transform: 'rotate(0deg) translateX(200px) rotate(0deg)',
            opacity: '0.8'
          },
          '50%': { opacity: '1' },
          '100%': { 
            transform: 'rotate(360deg) translateX(200px) rotate(-360deg)',
            opacity: '0.8'
          }
        }
      },
      backgroundImage: {
        'space-gradient': 'linear-gradient(135deg, #0a0a0a 0%, #1e1b2c 35%, #2d1b69 100%)',
        'earth-gradient': 'linear-gradient(45deg, #0ea5e9 0%, #10b981 50%, #f59e0b 100%)',
        'aurora-gradient': 'linear-gradient(45deg, #06b6d4 0%, #8b5cf6 50%, #ec4899 100%)',
        'cosmic-gradient': 'linear-gradient(135deg, #1e3a8a 0%, #7c3aed 50%, #db2777 100%)',
        'stars': 'radial-gradient(2px 2px at 20px 30px, #eee, transparent), radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.8), transparent)'
      },
      backdropBlur: {
        'xs': '2px',
        'sm': '4px',
        'md': '8px',
        'lg': '12px',
        'xl': '16px',
        '2xl': '24px',
        '3xl': '32px'
      },
      boxShadow: {
        'space': '0 25px 50px -12px rgba(0, 0, 0, 0.8)',
        'cosmic': '0 0 30px rgba(14, 165, 233, 0.3)',
        'earth': '0 0 25px rgba(16, 185, 129, 0.4)',
        'aurora': '0 0 35px rgba(167, 85, 247, 0.5)',
        'glow': '0 0 20px rgba(255, 255, 255, 0.1)',
        'inner-glow': 'inset 0 0 20px rgba(14, 165, 233, 0.2)'
      },
      borderRadius: {
        'space': '16px',
        'cosmic': '20px'
      }
    },
  },
  plugins: [],
}
