#!/usr/bin/env python3
"""Quick start script for Task Manager application."""

import os
import sys
import subprocess
import time
from pathlib import Path


def run_command(command, description, check=True):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"Command: {command}")
    print('='*60)
    
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        print("✅ SUCCESS")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FAILED")
        print(f"Error: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def main():
    """Main function to start the application."""
    print("🚀 Task Manager - Quick Start")
    print("="*60)
    
    # Check if we're in the right directory
    if not Path("app").exists():
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Check if .env exists
    if not Path(".env").exists():
        print("📝 Creating .env file from template...")
        if Path("env.example").exists():
            run_command("copy env.example .env", "Copy environment template")
        else:
            print("❌ Error: env.example not found")
            sys.exit(1)
    
    # Check if virtual environment exists
    if not Path(".venv").exists():
        print("📦 Creating virtual environment...")
        run_command("python -m venv .venv", "Create virtual environment")
    
    # Install dependencies
    print("📦 Installing dependencies...")
    if not run_command(".venv\\Scripts\\python.exe -m pip install -r requirements.txt", "Install dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Run migrations
    print("🗄️ Setting up database...")
    run_command(".venv\\Scripts\\python.exe -m alembic upgrade head", "Run database migrations")
    
    # Start application
    print("\n🚀 Starting Task Manager application...")
    print("📖 API Documentation will be available at: http://localhost:8000/docs")
    print("🔗 Application URL: http://localhost:8000")
    print("\nPress Ctrl+C to stop the application")
    
    run_command(".venv\\Scripts\\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload", 
               "Start FastAPI application", check=False)


if __name__ == "__main__":
    main()

