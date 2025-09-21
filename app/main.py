from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import auth, courses, tasks, calendar, files
from app.routers.ai import router as ai_router

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title="SUMA LMS API",
    description="Next-Generation Learning Management System API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加受信任主机中间件
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # 生产环境中请正确配置
)

# 包含路由 - 添加API版本前缀
app.include_router(auth.router, prefix="/api/v1")
app.include_router(courses.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(calendar.router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")  # 使用新的多智能体AI路由
app.include_router(files.router, prefix="/api/v1")


@app.get("/")
async def root():
    """根端点"""
    return {
        "message": "Welcome to SUMA LMS API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "redoc": "/api/redoc",
        "frontend": settings.frontend_url
    }


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "message": "SUMA LMS API is running"}


@app.get("/api/health")
async def api_health_check():
    """API健康检查端点"""
    return {"status": "healthy", "message": "SUMA LMS API is running"}


# 全局异常处理器
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"detail": "资源未找到"}


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"detail": "内部服务器错误"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
