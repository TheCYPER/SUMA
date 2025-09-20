# Ollama 设置指南

SUMA LMS 现在使用 Ollama 作为本地 AI 模型服务。请按照以下步骤设置 Ollama。

## 🚀 安装 Ollama

### macOS
```bash
# 使用 Homebrew 安装
brew install ollama

# 或者下载安装包
# 访问 https://ollama.ai 下载 macOS 安装包
```

### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows
访问 https://ollama.ai 下载 Windows 安装包

## 🔧 启动 Ollama 服务

```bash
# 启动 Ollama 服务
ollama serve
```

服务将在 `http://localhost:11434` 上运行。

## 📦 下载推荐模型

### 轻量级模型（推荐用于开发）
```bash
# Llama 3.2 (3B) - 快速且高效
ollama pull llama3.2

# 或者使用更小的模型
ollama pull phi3
```

### 更强大的模型（需要更多资源）
```bash
# Llama 3.1 (8B) - 更好的性能
ollama pull llama3.1

# 或者 Llama 3.1 (70B) - 最佳性能（需要大量内存）
ollama pull llama3.1:70b
```

## ⚙️ 配置 SUMA LMS

### 1. 设置环境变量
创建 `.env` 文件：
```bash
cp env.example .env
```

编辑 `.env` 文件：
```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

### 2. 验证设置
启动 SUMA LMS 后，访问：
- AI 状态检查：`http://localhost:8000/ai/status`
- API 文档：`http://localhost:8000/docs`

## 🧪 测试 AI 功能

### 1. 检查 Ollama 状态
```bash
curl http://localhost:8000/ai/status
```

### 2. 测试 AI 查询
```bash
# 登录获取 token
curl -X POST "http://localhost:8000/auth/login-json" \
  -H "Content-Type: application/json" \
  -d '{"username": "student1", "password": "student123"}'

# 使用 token 查询 AI
curl -X POST "http://localhost:8000/ai/query" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "你好，请介绍一下我的学习进度"}'
```

## 🔍 故障排除

### Ollama 服务未运行
```bash
# 检查 Ollama 是否在运行
ps aux | grep ollama

# 启动 Ollama 服务
ollama serve
```

### 模型未下载
```bash
# 查看已下载的模型
ollama list

# 下载默认模型
ollama pull llama3.2
```

### 端口冲突
如果端口 11434 被占用：
```bash
# 查看端口使用情况
lsof -i :11434

# 修改 Ollama 端口
OLLAMA_HOST=0.0.0.0:11435 ollama serve
```

然后更新 `.env` 文件中的 `OLLAMA_BASE_URL`。

## 📊 性能优化

### 内存使用
- **llama3.2 (3B)**: 约 2GB RAM
- **llama3.1 (8B)**: 约 5GB RAM
- **llama3.1 (70B)**: 约 40GB RAM

### GPU 加速
如果有 NVIDIA GPU：
```bash
# 安装 CUDA 版本的 Ollama
# 详见 https://ollama.ai/docs/gpu
```

## 🎯 推荐配置

### 开发环境
- 模型：`llama3.2` 或 `phi3`
- 内存：至少 4GB 可用
- 存储：至少 2GB 可用空间

### 生产环境
- 模型：`llama3.1` 或 `llama3.1:70b`
- 内存：至少 8GB 可用
- GPU：推荐使用 NVIDIA GPU

## 🔄 更新模型

```bash
# 更新特定模型
ollama pull llama3.2

# 删除旧模型
ollama rm llama3.2:old-tag
```

---

**现在你可以享受本地 AI 助手的强大功能了！** 🎉
