#!/usr/bin/env python3
"""
SUMA LMS Server Runner
This script starts the FastAPI development server
"""

import uvicorn
import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.dirname(__file__))

if __name__ == "__main__":
    print("🚀 Starting SUMA LMS API Server...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("📖 ReDoc Documentation: http://localhost:8000/redoc")
    print("🔧 Health Check: http://localhost:8000/health")
    print("\n" + "="*50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
