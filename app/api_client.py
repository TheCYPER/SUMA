"""
API客户端配置
为React前端提供统一的API调用接口
"""
from typing import Optional
import httpx
from app.config import settings


class APIClient:
    """API客户端类"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=30.0,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
    
    async def close(self):
        """关闭客户端连接"""
        await self.client.aclose()
    
    def set_auth_token(self, token: str):
        """设置认证token"""
        self.client.headers.update({"Authorization": f"Bearer {token}"})
    
    def remove_auth_token(self):
        """移除认证token"""
        if "Authorization" in self.client.headers:
            del self.client.headers["Authorization"]
    
    async def get(self, endpoint: str, **kwargs):
        """GET请求"""
        return await self.client.get(f"/api/v1{endpoint}", **kwargs)
    
    async def post(self, endpoint: str, **kwargs):
        """POST请求"""
        return await self.client.post(f"/api/v1{endpoint}", **kwargs)
    
    async def put(self, endpoint: str, **kwargs):
        """PUT请求"""
        return await self.client.put(f"/api/v1{endpoint}", **kwargs)
    
    async def delete(self, endpoint: str, **kwargs):
        """DELETE请求"""
        return await self.client.delete(f"/api/v1{endpoint}", **kwargs)
    
    async def patch(self, endpoint: str, **kwargs):
        """PATCH请求"""
        return await self.client.patch(f"/api/v1{endpoint}", **kwargs)


# 创建全局API客户端实例
api_client = APIClient()
