"""
Development Server Runner for Earth Observation Visualizer Backend
"""

import sys
import subprocess
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI dependencies found")
    except ImportError:
        print("❌ Missing dependencies. Installing...")
        os.system("pip install -r requirements.txt")

def create_env_file():
    """Create .env file from example if it doesn't exist"""
    env_file = Path(".env")
    example_file = Path("env.example")
    
    if not env_file.exists() and example_file.exists():
        print("📝 Creating .env file from template...")
        env_content = example_file.read_text()
        env_file.write_text(env_content)
        print("✅ .env file created. Please edit with your API keys.")

def check_env_variables():
    """Check if environment variables are configured"""
    env_file = Path(".env")
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            if 'your_nasa_api_key_here' in content:
                print(
                    "⚠️  API keys not configured. "
                    "Please edit .env file with your NASA/Mapbox credentials for real data.\n"
                    "Continuing with mock data mode..."
                )
            else:
                print("✅ Environment variables configured")
    else:
        print("⚠️  .env file not found. Using default settings...")

def start_server():
    """Start the FastAPI development server"""
    # Add the backend directory to sys.path to resolve module import issues
    sys.path.insert(0, str(Path(__file__).parent.absolute()))
    
    print("\n🚀 Starting Earth Observation Visualizer Backend...")
    print("📍 Server URL: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/api/docs")
    print("🛡️  Running in development mode with mock data\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--log-level", "info"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

def main():
    """Main function to setup and start the backend"""
    print("🌍 Earth Observation Visualizer - Backend Setup")
    print("=" * 50)
    
    check_requirements()
    create_env_file()
    check_env_variables()
    
    print("\n🔧 Backend Configuration:")
    print("   • FastAPI server with async support")
    print("   • NASA Earth Observation API integration ready")
    print("   • Environmental data simulation")
    print("   • Interactive documentation")
    print("   • CORS enabled for frontend")
    
    start_server()

if __name__ == "__main__":
    main()
