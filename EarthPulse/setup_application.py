#!/usr/bin/env python3
"""
Earth Observation Visualizer - Complete Setup Script
Integrates NASA API and configures the full application
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=shell, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error running command: {command}")
            print(f"Error: {result.stderr}")
            return False
        print(f"✅ Success: {command}")
        return True
    except Exception as e:
        print(f"❌ Exception running command: {command}")
        print(f"Error: {e}")
        return False

def setup_directories():
    """Create necessary directories"""
    directories = [
        "backend/logs",
        "backend/uploads", 
        "backend/reports",
        "backend/cache",
        "backend/static"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def install_backend_dependencies():
    """Install Python backend dependencies"""
    print("🐍 Installing Python backend dependencies...")
    
    # Check if Python is available
    if not run_command("python --version"):
        print("❌ Python not found. Please install Python 3.11+")
        return False
    
    # Install dependencies
    if not run_command("pip install -r backend/requirements.txt"):
        print("❌ Failed to install backend dependencies")
        return False
    
    print("✅ Backend dependencies installed successfully")
    return True

def install_frontend_dependencies():
    """Install Node.js frontend dependencies"""
    print("📦 Installing Node.js frontend dependencies...")
    
    # Check if Node.js is available
    if not run_command("node --version"):
        print("❌ Node.js not found. Please install Node.js 18+")
        return False
    
    # Check if npm is available
    if not run_command("npm --version"):
        print("❌ npm not found. Please install npm")
        return False
    
    # Install dependencies
    if not run_command("npm install"):
        print("❌ Failed to install frontend dependencies")
        return False
    
    print("✅ Frontend dependencies installed successfully")
    return True

def configure_nasa_api(nasa_token):
    """Configure NASA API token in environment files"""
    print("🚀 Configuring NASA API integration...")
    
    # Update backend environment
    backend_env_path = "backend/env.production"
    if os.path.exists(backend_env_path):
        with open(backend_env_path, 'r') as f:
            content = f.read()
        
        # Replace NASA API key
        content = content.replace("your_nasa_api_key_here", nasa_token)
        content = content.replace("USE_MOCK_DATA=false", "USE_MOCK_DATA=false")
        
        with open(backend_env_path, 'w') as f:
            f.write(content)
        
        print("✅ NASA API token configured in backend")
    
    # Update frontend environment
    frontend_env_path = "frontend.env.local"
    if os.path.exists(frontend_env_path):
        with open(frontend_env_path, 'r') as f:
            content = f.read()
        
        # Update API configuration
        content = content.replace("VITE_MOCK_DATA_ENABLED=false", "VITE_MOCK_DATA_ENABLED=false")
        
        with open(frontend_env_path, 'w') as f:
            f.write(content)
        
        print("✅ Frontend environment configured")
    
    return True

def create_startup_scripts():
    """Create startup scripts for easy development"""
    
    # Backend startup script
    backend_script = """#!/bin/bash
# Backend startup script
echo "🚀 Starting Earth Observation Visualizer Backend..."
cd backend
export PYTHONPATH=$PWD
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
"""
    
    with open("start_backend.sh", "w") as f:
        f.write(backend_script)
    
    # Make executable
    os.chmod("start_backend.sh", 0o755)
    
    # Frontend startup script
    frontend_script = """#!/bin/bash
# Frontend startup script
echo "🌐 Starting Earth Observation Visualizer Frontend..."
npm run dev
"""
    
    with open("start_frontend.sh", "w") as f:
        f.write(frontend_script)
    
    # Make executable
    os.chmod("start_frontend.sh", 0o755)
    
    print("✅ Startup scripts created")

def test_backend():
    """Test backend API server"""
    print("🧪 Testing backend API server...")
    
    # Start backend in background
    backend_process = subprocess.Popen(
        ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd="backend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait a moment for server to start
    import time
    time.sleep(5)
    
    # Test API endpoint
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend API server is running successfully")
            backend_process.terminate()
            return True
        else:
            print(f"❌ Backend API test failed: {response.status_code}")
            backend_process.terminate()
            return False
    except Exception as e:
        print(f"❌ Backend API test failed: {e}")
        backend_process.terminate()
        return False

def main():
    """Main setup function"""
    print("🌍 Earth Observation Visualizer - Complete Setup")
    print("=" * 60)
    
    # Get NASA API token from user
    nasa_token = input("🔑 Please enter your NASA API token: ").strip()
    if not nasa_token:
        print("❌ NASA API token is required")
        return False
    
    print(f"✅ NASA API token received: {nasa_token[:10]}...")
    
    # Setup steps
    steps = [
        ("Creating directories", setup_directories),
        ("Installing backend dependencies", install_backend_dependencies),
        ("Installing frontend dependencies", install_frontend_dependencies),
        ("Configuring NASA API", lambda: configure_nasa_api(nasa_token)),
        ("Creating startup scripts", create_startup_scripts),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            print(f"❌ Failed: {step_name}")
            return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start backend: ./start_backend.sh")
    print("2. Start frontend: ./start_frontend.sh")
    print("3. Open http://localhost:3000 in your browser")
    print("\n🔧 Configuration files:")
    print("- Backend: backend/env.production")
    print("- Frontend: frontend.env.local")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
