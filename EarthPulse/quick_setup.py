#!/usr/bin/env python3
"""
Quick Setup for Earth Observation Visualizer
Gets NASA API token and starts the application
"""

import os
import sys
import subprocess
import time

def get_nasa_token():
    """Get NASA API token from user"""
    print("🌍 Earth Observation Visualizer - NASA API Setup")
    print("=" * 60)
    print()
    print("🔑 To get your NASA Earthdata token:")
    print("1. Go to: https://urs.earthdata.nasa.gov/")
    print("2. Create an account (if you don't have one)")
    print("3. Go to 'Applications' → 'Create Application'")
    print("4. Copy your 'Bearer Token'")
    print()
    
    token = input("🔑 Enter your NASA Earthdata Bearer Token: ").strip()
    
    if not token:
        print("❌ NASA token is required for real satellite data")
        return None
    
    if len(token) < 50:
        print("⚠️  Token seems too short. Make sure you copied the full Bearer token.")
        confirm = input("Continue anyway? (y/n): ").lower()
        if confirm != 'y':
            return None
    
    return token

def configure_environment(token):
    """Configure environment files with NASA token"""
    print("⚙️  Configuring environment files...")
    
    # Update backend environment
    backend_env = "backend/env.production"
    if os.path.exists(backend_env):
        with open(backend_env, 'r') as f:
            content = f.read()
        
        content = content.replace("your_nasa_api_key_here", token)
        content = content.replace("USE_MOCK_DATA=false", "USE_MOCK_DATA=false")
        
        with open(backend_env, 'w') as f:
            f.write(content)
        
        print("✅ Backend environment configured")
    
    # Update frontend environment
    frontend_env = "frontend.env.local"
    if os.path.exists(frontend_env):
        with open(frontend_env, 'r') as f:
            content = f.read()
        
        content = content.replace("VITE_MOCK_DATA_ENABLED=false", "VITE_MOCK_DATA_ENABLED=false")
        
        with open(frontend_env, 'w') as f:
            f.write(content)
        
        print("✅ Frontend environment configured")

def install_dependencies():
    """Install all dependencies"""
    print("📦 Installing dependencies...")
    
    # Install backend dependencies
    print("🐍 Installing Python dependencies...")
    result = subprocess.run([
        "pip", "install", "-r", "backend/requirements.txt"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Failed to install Python dependencies: {result.stderr}")
        return False
    
    print("✅ Python dependencies installed")
    
    # Install frontend dependencies
    print("📦 Installing Node.js dependencies...")
    result = subprocess.run([
        "npm", "install"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Failed to install Node.js dependencies: {result.stderr}")
        return False
    
    print("✅ Node.js dependencies installed")
    return True

def start_application():
    """Start the application"""
    print("🚀 Starting Earth Observation Visualizer...")
    print()
    print("📋 Application will be available at:")
    print("🌐 Frontend: http://localhost:3000")
    print("📡 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/api/docs")
    print()
    print("💡 Press Ctrl+C to stop the application")
    print()
    
    # Start the application using the startup script
    try:
        subprocess.run([sys.executable, "start_application.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

def main():
    """Main setup function"""
    try:
        # Get NASA token
        token = get_nasa_token()
        if not token:
            print("❌ Setup cancelled")
            return False
        
        # Configure environment
        configure_environment(token)
        
        # Install dependencies
        if not install_dependencies():
            print("❌ Failed to install dependencies")
            return False
        
        print("✅ Setup completed successfully!")
        print()
        
        # Start application
        start_application()
        
        return True
        
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled by user")
        return False
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

