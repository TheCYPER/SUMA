from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import auth, courses, tasks, calendar, ai, files

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title="SUMA LMS API",
    description="下一代学习管理系统API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
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

# 包含路由
app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(tasks.router)
app.include_router(calendar.router)
app.include_router(ai.router)
app.include_router(files.router)


@app.get("/")
async def root():
    """根端点"""
    return {
        "message": "欢迎使用SUMA LMS API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "message": "SUMA LMS API正在运行"}


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
