# SUMA - 下一代学习管理系统

SUMA是一个现代化的、AI驱动的学习管理系统，使用FastAPI和Ollama构建，旨在为学生和教师提供直观高效的学习体验。

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Ollama](https://img.shields.io/badge/Ollama-AI%20Powered-purple.svg)](https://ollama.ai)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ 功能特性

### 🎯 核心功能
- **👥 用户管理**: 学生、教师和管理员角色，支持JWT认证
- **📚 课程管理**: 创建和管理课程，支持自定义图标和颜色
- **📝 任务管理**: 作业、测试、实验、项目和测验
- **📁 文件上传/下载**: 支持多种文件类型，具备预览功能
- **📅 日历集成**: 周历视图，支持.ics导出
- **🤖 AI助手**: 使用Ollama的本地AI智能帮助
- **📊 仪表板**: 个性化仪表板，显示统计数据和即将到期的任务

### 🚀 高级功能
- **🔔 实时通知**: 任务截止日期和公告提醒
- **📈 成绩管理**: 跟踪成绩和课程进度
- **📋 考勤跟踪**: 监控学生出勤情况
- **📖 资源管理**: 分享课程材料和资源
- **🎨 主题定制**: 个性化界面
- **📱 移动响应**: 在所有设备上无缝工作

## 🛠️ 技术栈

### 后端
- **FastAPI**: 现代化、快速的Web框架
- **SQLAlchemy**: SQL工具包和ORM
- **SQLite**: 轻量级数据库（可轻松升级到PostgreSQL）
- **Alembic**: 数据库迁移工具
- **Ollama**: 本地AI模型集成
- **JWT**: 安全认证
- **Pydantic**: 数据验证和设置管理

### AI集成
- **Ollama**: 本地AI模型服务器
- **Llama 3.1**: 大型语言模型，提供智能帮助
- **中文语言支持**: 原生中文语言处理

## 🚀 快速开始

### 前置要求
- Python 3.8+
- [Ollama](https://ollama.ai)（用于AI功能）

### 1. 克隆仓库
```bash
git clone https://github.com/your-username/suma-lms.git
cd suma-lms
```

### 2. 设置环境
```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境
```bash
# 复制环境模板
cp env.example .env

# 编辑.env文件，设置你的配置
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_MODEL=llama3.1:8b
```

### 4. 设置Ollama（用于AI功能）
```bash
# 安装Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 启动Ollama服务
ollama serve

# 拉取模型（在另一个终端中）
ollama pull llama3.1:8b
```

### 5. 初始化数据库
```bash
python init_db.py
```

### 6. 启动服务器
```bash
python -m app.main
```

API将在 `http://localhost:8000` 可用

## 📚 API文档

服务器运行后，你可以访问：
- **交互式API文档**: http://localhost:8000/docs
- **ReDoc文档**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/health

## 🔧 配置

### 环境变量

创建`.env`文件，包含以下变量：

```env
# 数据库
DATABASE_URL=sqlite:///./suma.db

# 安全
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Ollama配置
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# 文件上传
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760  # 10MB

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### 默认测试账户

运行`init_db.py`后，你将拥有这些测试账户：

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | `admin` | `admin123` |
| 教师 | `teacher` | `teacher123` |
| 学生 | `student1` | `student123` |
| 学生 | `student2` | `student123` |

## 🧪 测试

### 运行API测试
```bash
# 测试所有功能
python test_api_complete.py

# 测试Ollama连接
python test_ollama.py

# 测试特定API端点
python test_api.py
```

### 测试AI功能
```bash
# 检查AI状态
curl http://localhost:8000/ai/status

# 测试AI查询（登录后）
curl -X POST "http://localhost:8000/ai/query" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "你好，请介绍一下我的学习进度"}'
```

## 🏗️ 项目结构

```
Suma/
├── app/                    # 主应用代码
│   ├── routers/           # API路由处理器
│   │   ├── auth.py        # 认证端点
│   │   ├── courses.py     # 课程管理
│   │   ├── tasks.py       # 任务管理
│   │   ├── calendar.py    # 日历和事件
│   │   ├── ai.py          # AI助手（Ollama）
│   │   └── files.py       # 文件上传/下载
│   ├── models.py          # SQLAlchemy数据库模型
│   ├── schemas.py         # Pydantic数据模式
│   ├── crud.py           # 数据库操作
│   ├── auth.py           # 认证逻辑
│   ├── config.py         # 配置设置
│   ├── database.py       # 数据库连接
│   ├── utils.py          # 工具函数
│   └── main.py           # FastAPI应用
├── alembic/              # 数据库迁移
├── .github/workflows/    # CI/CD管道
├── uploads/              # 文件上传目录
├── requirements.txt      # Python依赖
├── env.example          # 环境变量模板
├── init_db.py           # 数据库初始化
├── test_*.py            # 测试脚本
├── Dockerfile           # 容器配置
├── docker-compose.yml   # 多容器设置
├── OLLAMA_SETUP.md      # Ollama设置指南
├── QUICKSTART.md        # 快速开始指南
├── DEPLOYMENT.md        # 部署指南
├── CONTRIBUTING.md      # 贡献指南
└── README.md            # 项目文档
```

## 🔌 主要API端点

### 认证
- `POST /auth/register` - 注册新用户
- `POST /auth/login-json` - 用户登录
- `GET /auth/me` - 获取当前用户信息

### 课程
- `GET /courses/` - 获取用户课程
- `POST /courses/` - 创建新课程（教师/管理员）
- `GET /courses/{id}` - 获取课程详情
- `POST /courses/{id}/enroll` - 注册课程

### 任务
- `GET /tasks/` - 获取用户任务
- `GET /tasks/upcoming` - 获取即将到期的任务
- `POST /tasks/` - 创建任务（教师/管理员）
- `GET /tasks/{id}` - 获取任务详情
- `POST /tasks/{id}/submission` - 提交任务

### AI助手
- `GET /ai/status` - 检查AI助手状态
- `POST /ai/query` - 查询AI助手
- `GET /ai/dashboard-summary` - 获取AI仪表板摘要
- `POST /ai/task-analysis` - 分析任务文件
- `GET /ai/study-tips` - 获取个性化学习建议

### 日历和仪表板
- `GET /calendar/events` - 获取日历事件
- `GET /calendar/export/ics` - 导出日历为.ics格式
- `GET /calendar/dashboard` - 获取仪表板数据

### 文件
- `POST /files/upload` - 上传文件
- `GET /files/download/{path}` - 下载文件
- `GET /files/preview/{path}` - 预览文件

## 🚀 部署

### 开发环境
```bash
python -m app.main
```

### 生产环境
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker（即将推出）
```bash
docker build -t suma-lms .
docker run -p 8000:8000 suma-lms
```

## 🤖 AI功能

SUMA LMS包含由Ollama驱动的强大AI助手：

- **本地AI**: 无需外部API密钥
- **中文支持**: 原生中文语言处理
- **智能建议**: 上下文感知推荐
- **任务分析**: 分析上传文件并提供洞察
- **学习建议**: 个性化学习策略
- **进度跟踪**: AI驱动的学术进度分析

## 🤝 贡献

我们欢迎贡献！请查看我们的[贡献指南](CONTRIBUTING.md)了解详情。

1. Fork仓库
2. 创建功能分支（`git checkout -b feature/amazing-feature`）
3. 提交更改（`git commit -m 'Add amazing feature'`）
4. 推送到分支（`git push origin feature/amazing-feature`）
5. 打开Pull Request

## 📝 许可证

本项目采用MIT许可证 - 查看[LICENSE](LICENSE)文件了解详情。

## 🆘 支持

如果遇到问题或有疑问：

1. 查看[API文档](http://localhost:8000/docs)
2. 查看[Issues](https://github.com/your-username/suma-lms/issues)页面
3. 创建新issue并提供详细信息
4. 查看[OLLAMA_SETUP.md](OLLAMA_SETUP.md)获取AI设置帮助

## 🔮 路线图

### 第一阶段 ✅（当前）
- ✅ 具有核心功能的后端API
- ✅ 数据库模型和认证
- ✅ 文件上传/下载系统
- ✅ Ollama AI助手集成
- ✅ 中文语言支持

### 第二阶段 🔄（下一步）
- 🔄 Next.js前端
- 🔄 实时通知
- 🔄 高级日历功能
- 🔄 移动应用

### 第三阶段 📋（未来）
- 📋 视频会议集成
- 📋 高级分析
- 📋 多语言支持
- 📋 插件系统
- 📋 高级AI功能

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - Web框架
- [Ollama](https://ollama.ai/) - 本地AI模型服务器
- [SQLAlchemy](https://sqlalchemy.org/) - 数据库ORM
- [Pydantic](https://pydantic.dev/) - 数据验证

---

**SUMA LMS** - 通过技术赋能教育 🎓

*为学习的未来而构建 ❤️*
