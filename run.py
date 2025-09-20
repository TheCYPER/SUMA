#!/usr/bin/env python3
"""
SUMA LMS服务器运行器
此脚本启动FastAPI开发服务器
"""

import uvicorn
import os
import sys

# 将应用目录添加到Python路径
sys.path.append(os.path.dirname(__file__))

if __name__ == "__main__":
    print("🚀 正在启动SUMA LMS API服务器...")
    print("📚 API文档: http://localhost:8000/docs")
    print("📖 ReDoc文档: http://localhost:8000/redoc")
    print("🔧 健康检查: http://localhost:8000/health")
    print("\n" + "="*50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
