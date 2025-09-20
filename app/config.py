from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # 数据库配置
    database_url: str = "sqlite:///./suma.db"
    
    # 安全配置
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Ollama AI配置
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"  # 默认模型，可以更改
    
    # 文件上传配置
    upload_dir: str = "./uploads"
    max_file_size: int = 10485760  # 10MB
    
    # 跨域配置
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# 创建配置实例
settings = Settings()

# 确保上传目录存在
os.makedirs(settings.upload_dir, exist_ok=True)
