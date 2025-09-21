# SUMA LMS 项目结构说明

## 📁 项目整体结构

```
Suma/
├── app/                    # 后端应用
│   ├── routers/           # API路由
│   │   ├── auth.py        # 认证相关API
│   │   ├── courses.py     # 课程管理API
│   │   ├── tasks.py       # 任务管理API
│   │   ├── calendar.py    # 日历和事件API
│   │   ├── ai.py          # AI助手API
│   │   └── files.py       # 文件管理API
│   ├── models.py          # 数据库模型
│   ├── schemas.py         # Pydantic数据模式
│   ├── crud.py           # 数据库操作
│   ├── auth.py           # 认证逻辑
│   ├── config.py         # 配置管理
│   ├── database.py       # 数据库连接
│   ├── utils.py          # 工具函数
│   ├── api_client.py     # API客户端（新增）
│   └── main.py           # FastAPI应用入口
├── frontend/              # React前端应用
│   ├── src/
│   │   ├── components/    # React组件
│   │   │   ├── Layout.tsx
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── LoadingSpinner.tsx
│   │   ├── pages/         # 页面组件
│   │   │   ├── Dashboard.tsx
│   │   │   └── Login.tsx
│   │   ├── contexts/      # React上下文
│   │   │   └── AuthContext.tsx
│   │   ├── services/      # API服务
│   │   │   └── api.ts
│   │   ├── types/         # TypeScript类型
│   │   │   └── index.ts
│   │   ├── hooks/         # 自定义Hooks
│   │   ├── utils/         # 工具函数
│   │   ├── App.tsx        # 主应用组件
│   │   └── main.tsx       # 应用入口
│   ├── public/            # 静态资源
│   ├── package.json       # 前端依赖
│   ├── tailwind.config.js # Tailwind配置
│   ├── postcss.config.js  # PostCSS配置
│   ├── vite.config.ts     # Vite配置
│   ├── Dockerfile         # 前端Docker配置
│   └── nginx.conf         # Nginx配置
├── alembic/              # 数据库迁移
├── uploads/              # 文件上传目录
├── requirements.txt      # Python依赖
├── env.example          # 环境变量模板
├── init_db.py           # 数据库初始化
├── start-dev.sh         # 开发环境启动脚本
├── docker-compose.yml   # Docker Compose配置
├── Dockerfile           # 后端Docker配置
└── README.md            # 项目文档
```

## 🔧 后端结构优化

### 主要改进
1. **API版本控制**: 所有API路由添加 `/api/v1` 前缀
2. **CORS配置**: 支持React前端跨域请求
3. **配置管理**: 添加前端URL和环境配置
4. **API客户端**: 创建统一的API调用接口

### 新增文件
- `app/api_client.py`: 统一的API客户端类
- 更新 `app/config.py`: 添加前端相关配置
- 更新 `app/main.py`: 支持API版本控制和CORS

## 🎨 前端结构

### 技术栈
- **React 18**: 现代前端框架
- **TypeScript**: 类型安全
- **Vite**: 快速构建工具
- **Tailwind CSS**: 实用优先的CSS框架
- **React Router**: 客户端路由
- **React Query**: 数据获取和缓存
- **Axios**: HTTP客户端

### 项目结构
```
frontend/
├── src/
│   ├── components/       # 可复用组件
│   │   ├── Layout.tsx    # 布局组件
│   │   ├── Header.tsx    # 头部组件
│   │   ├── Sidebar.tsx   # 侧边栏组件
│   │   └── LoadingSpinner.tsx # 加载组件
│   ├── pages/            # 页面组件
│   │   ├── Dashboard.tsx # 仪表板页面
│   │   └── Login.tsx     # 登录页面
│   ├── contexts/         # React上下文
│   │   └── AuthContext.tsx # 认证上下文
│   ├── services/         # API服务
│   │   └── api.ts        # API调用封装
│   ├── types/            # TypeScript类型
│   │   └── index.ts      # 类型定义
│   ├── hooks/            # 自定义Hooks
│   ├── utils/            # 工具函数
│   ├── App.tsx           # 主应用组件
│   └── main.tsx          # 应用入口
├── public/               # 静态资源
├── package.json          # 依赖管理
├── tailwind.config.js    # Tailwind配置
├── postcss.config.js     # PostCSS配置
├── vite.config.ts        # Vite配置
├── Dockerfile            # Docker配置
└── nginx.conf            # Nginx配置
```

## 🚀 开发环境

### 快速启动
```bash
# 使用开发脚本（推荐）
./start-dev.sh

# 或手动启动
# 后端
python -m app.main

# 前端
cd frontend && npm run dev
```

### 访问地址
- **前端**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/api/docs
- **Ollama**: http://localhost:11434

## 🐳 生产部署

### Docker Compose
```bash
# 启动所有服务
docker-compose up -d

# 初始化数据库
docker-compose exec suma-lms python init_db.py
```

### 服务说明
- **suma-lms**: 后端API服务 (端口8000)
- **frontend**: React前端服务 (端口3000)
- **ollama**: AI模型服务 (端口11434)
- **postgres**: 数据库服务 (端口5432, 可选)

## 📝 配置说明

### 环境变量
```env
# 数据库
DATABASE_URL=sqlite:///./suma.db

# 安全
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Ollama AI
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# 文件上传
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760

# CORS - 支持React前端
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# 前端配置
FRONTEND_URL=http://localhost:3000

# 环境
ENVIRONMENT=development
DEBUG=true
```

## 🔄 API版本控制

所有API端点现在使用版本前缀：
- 旧格式: `/auth/login`
- 新格式: `/api/v1/auth/login`

这确保了API的向后兼容性和版本管理。

## 🎯 下一步开发

### 前端页面开发
1. 课程管理页面
2. 任务管理页面
3. 日历页面
4. AI助手页面
5. 用户管理页面（管理员）

### 功能增强
1. 实时通知（WebSocket）
2. 文件预览功能
3. 移动端适配
4. 主题切换
5. 多语言支持

### 性能优化
1. 代码分割
2. 图片优化
3. 缓存策略
4. 懒加载

---

**项目结构已优化完成，支持前后端分离开发！** 🎉
