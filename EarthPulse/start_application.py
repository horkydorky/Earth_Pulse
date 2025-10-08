#!/usr/bin/env python3
"""
Earth Observation Visualizer - Application Startup Script
Starts both backend and frontend servers with NASA API integration
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

class ApplicationManager:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print("\n🛑 Shutting down application...")
        self.running = False
        self.stop_servers()
        sys.exit(0)
    
    def start_backend(self):
        """Start the FastAPI backend server"""
        print("🚀 Starting Earth Observation Visualizer Backend...")
        
        try:
            # Change to backend directory
            backend_dir = Path("backend")
            if not backend_dir.exists():
                print("❌ Backend directory not found")
                return False
            
            # Set environment variables
            env = os.environ.copy()
            env["PYTHONPATH"] = str(backend_dir.absolute())
            
            # Start uvicorn server
            self.backend_process = subprocess.Popen(
                [
                    "python", "-m", "uvicorn", 
                    "app.main:app", 
                    "--host", "0.0.0.0", 
                    "--port", "8000", 
                    "--reload"
                ],
                cwd=backend_dir,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            # Wait for backend to start
            print("⏳ Waiting for backend to start...")
            time.sleep(5)
            
            # Test backend health
            try:
                import requests
                response = requests.get("http://localhost:8000/health", timeout=10)
                if response.status_code == 200:
                    print("✅ Backend API server started successfully")
                    print("📡 Backend API: http://localhost:8000")
                    print("📚 API Documentation: http://localhost:8000/api/docs")
                    return True
                else:
                    print(f"❌ Backend health check failed: {response.status_code}")
                    return False
            except Exception as e:
                print(f"❌ Backend health check failed: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False
    
    def start_frontend(self):
        """Start the React frontend server"""
        print("🌐 Starting Earth Observation Visualizer Frontend...")
        
        try:
            # Check if node_modules exists
            if not Path("node_modules").exists():
                print("📦 Installing frontend dependencies...")
                install_result = subprocess.run(
                    ["npm", "install"],
                    capture_output=True,
                    text=True
                )
                if install_result.returncode != 0:
                    print(f"❌ Failed to install frontend dependencies: {install_result.stderr}")
                    return False
                print("✅ Frontend dependencies installed")
            
            # Start npm dev server
            self.frontend_process = subprocess.Popen(
                ["npm", "run", "dev"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            # Wait for frontend to start
            print("⏳ Waiting for frontend to start...")
            time.sleep(8)
            
            print("✅ Frontend server started successfully")
            print("🌐 Frontend Application: http://localhost:3000")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
            return False
    
    def stop_servers(self):
        """Stop both backend and frontend servers"""
        if self.backend_process:
            print("🛑 Stopping backend server...")
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
        
        if self.frontend_process:
            print("🛑 Stopping frontend server...")
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
    
    def monitor_servers(self):
        """Monitor server processes"""
        while self.running:
            try:
                # Check backend
                if self.backend_process and self.backend_process.poll() is not None:
                    print("❌ Backend server stopped unexpectedly")
                    break
                
                # Check frontend
                if self.frontend_process and self.frontend_process.poll() is not None:
                    print("❌ Frontend server stopped unexpectedly")
                    break
                
                time.sleep(1)
                
            except KeyboardInterrupt:
                break
    
    def run(self):
        """Run the complete application"""
        print("🌍 Earth Observation Visualizer - Starting Application")
        print("=" * 60)
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Check prerequisites
        print("🔍 Checking prerequisites...")
        
        # Check Python
        try:
            result = subprocess.run(["python", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Python not found. Please install Python 3.11+")
                return False
            print(f"✅ Python: {result.stdout.strip()}")
        except Exception:
            print("❌ Python not found. Please install Python 3.11+")
            return False
        
        # Check Node.js
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Node.js not found. Please install Node.js 18+")
                return False
            print(f"✅ Node.js: {result.stdout.strip()}")
        except Exception:
            print("❌ Node.js not found. Please install Node.js 18+")
            return False
        
        # Check npm
        try:
            result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ npm not found. Please install npm")
                return False
            print(f"✅ npm: {result.stdout.strip()}")
        except Exception:
            print("❌ npm not found. Please install npm")
            return False
        
        print("\n🚀 Starting servers...")
        
        # Start backend
        if not self.start_backend():
            print("❌ Failed to start backend server")
            return False
        
        # Start frontend
        if not self.start_frontend():
            print("❌ Failed to start frontend server")
            self.stop_servers()
            return False
        
        print("\n🎉 Application started successfully!")
        print("\n📋 Access Points:")
        print("🌐 Frontend: http://localhost:3000")
        print("📡 Backend API: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/api/docs")
        print("\n💡 Press Ctrl+C to stop the application")
        
        # Monitor servers
        try:
            self.monitor_servers()
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_servers()
            print("\n👋 Application stopped. Goodbye!")
        
        return True

def main():
    """Main function"""
    manager = ApplicationManager()
    success = manager.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
