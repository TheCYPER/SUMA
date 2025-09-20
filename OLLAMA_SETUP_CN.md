# Ollama设置指南

本指南将帮助您在SUMA LMS中设置和使用Ollama AI功能。

## 什么是Ollama？

Ollama是一个本地AI模型服务器，允许您在本地运行大型语言模型，无需外部API密钥。它支持多种模型，包括Llama、CodeLlama、Mistral等。

## 安装Ollama

### macOS

```bash
# 使用Homebrew安装
brew install ollama

# 或者下载安装包
# 访问 https://ollama.ai 下载macOS安装包
```

### Linux

```bash
# 使用安装脚本
curl -fsSL https://ollama.ai/install.sh | sh

# 或者手动安装
# 访问 https://ollama.ai 下载Linux安装包
```

### Windows

1. 访问 [https://ollama.ai](https://ollama.ai)
2. 下载Windows安装包
3. 运行安装程序
4. 按照安装向导完成安装

## 启动Ollama服务

安装完成后，启动Ollama服务：

```bash
# 启动Ollama服务
ollama serve
```

服务将在 `http://localhost:11434` 运行。

## 下载模型

SUMA LMS推荐使用Llama 3.1模型。下载模型：

```bash
# 下载Llama 3.1 8B模型（推荐）
ollama pull llama3.1:8b

# 或者下载其他模型
ollama pull llama3.2:3b  # 更小的模型，适合资源有限的系统
ollama pull llama3.2:70b # 更大的模型，需要更多资源
```

## 验证安装

检查Ollama是否正常工作：

```bash
# 列出已安装的模型
ollama list

# 测试模型
ollama run llama3.1:8b
```

在交互式提示符中，输入一些文本测试模型响应。

## 配置SUMA LMS

### 1. 更新环境变量

确保您的`.env`文件包含正确的Ollama配置：

```env
# Ollama配置
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

### 2. 测试连接

启动SUMA LMS服务器后，测试AI功能：

```bash
# 检查AI状态
curl http://localhost:8000/ai/status

# 测试AI查询（需要先登录获取token）
curl -X POST "http://localhost:8000/ai/query" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "你好，请介绍一下我的学习进度"}'
```

## 可用模型

### 推荐模型

| 模型 | 大小 | 内存需求 | 性能 | 推荐用途 |
|------|------|----------|------|----------|
| llama3.1:8b | 8B | 8GB+ | 优秀 | 生产环境 |
| llama3.2:3b | 3B | 4GB+ | 良好 | 开发/测试 |
| llama3.2:70b | 70B | 40GB+ | 极佳 | 高性能需求 |

### 其他模型

```bash
# 代码生成模型
ollama pull codellama:7b

# 对话模型
ollama pull mistral:7b

# 中文模型
ollama pull qwen:7b
```

## 性能优化

### 系统要求

- **最低配置**: 4GB RAM, 2 CPU核心
- **推荐配置**: 8GB+ RAM, 4+ CPU核心
- **高性能配置**: 16GB+ RAM, 8+ CPU核心

### 优化设置

1. **调整模型大小**: 根据系统资源选择合适的模型
2. **GPU加速**: 如果有NVIDIA GPU，Ollama会自动使用CUDA
3. **内存管理**: 确保有足够的内存运行模型

## 故障排除

### 常见问题

1. **模型下载失败**
   ```bash
   # 检查网络连接
   ping ollama.ai
   
   # 重新下载模型
   ollama pull llama3.1:8b
   ```

2. **内存不足**
   ```bash
   # 使用更小的模型
   ollama pull llama3.2:3b
   
   # 或者释放内存
   ollama stop
   ollama start
   ```

3. **连接超时**
   ```bash
   # 检查Ollama服务状态
   ps aux | grep ollama
   
   # 重启服务
   ollama serve
   ```

4. **模型响应慢**
   - 检查系统资源使用情况
   - 考虑使用更小的模型
   - 确保有足够的可用内存

### 调试模式

启用详细日志：

```bash
# 启动Ollama并启用调试
OLLAMA_DEBUG=1 ollama serve

# 查看日志
tail -f ~/.ollama/logs/server.log
```

## 生产环境部署

### Docker部署

```yaml
# docker-compose.yml
version: '3.8'
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
    restart: unless-stopped

volumes:
  ollama_data:
```

### 系统服务

创建systemd服务文件：

```ini
# /etc/systemd/system/ollama.service
[Unit]
Description=Ollama Service
After=network.target

[Service]
Type=simple
User=ollama
Group=ollama
ExecStart=/usr/local/bin/ollama serve
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl enable ollama
sudo systemctl start ollama
```

## 安全考虑

1. **网络安全**: 在生产环境中，考虑使用防火墙限制访问
2. **访问控制**: 配置适当的用户权限
3. **资源限制**: 设置内存和CPU使用限制
4. **日志监控**: 监控Ollama服务日志

## 更新和维护

### 更新Ollama

```bash
# 更新Ollama
ollama update

# 或者重新安装
curl -fsSL https://ollama.ai/install.sh | sh
```

### 更新模型

```bash
# 更新特定模型
ollama pull llama3.1:8b

# 删除旧模型
ollama rm old-model-name
```

## 支持

如果遇到问题：

1. 查看[Ollama文档](https://ollama.ai/docs)
2. 检查[GitHub Issues](https://github.com/ollama/ollama/issues)
3. 查看SUMA LMS日志
4. 创建新的issue并提供详细信息

---

**AI功能设置完成！🤖**
