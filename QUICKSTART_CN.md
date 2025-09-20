# SUMA LMS 快速开始指南

本指南将帮助您快速启动和运行SUMA LMS。

## 前置要求

- Python 3.8或更高版本
- pip（Python包安装器）
- Git（用于克隆仓库）

## 步骤1：克隆仓库

```bash
git clone <repository-url>
cd suma-lms
```

## 步骤2：创建虚拟环境

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

## 步骤3：安装依赖

```bash
pip install -r requirements.txt
```

## 步骤4：设置环境变量

```bash
# 复制示例环境文件
cp env.example .env

# 编辑.env文件，设置你的配置
# 默认设置应该适用于本地开发
```

## 步骤5：初始化数据库

```bash
python init_db.py
```

这将创建数据库表并填充示例数据。

## 步骤6：启动服务器

```bash
python -m app.main
```

API将在 `http://localhost:8000` 可用

## 步骤7：访问API文档

打开浏览器并访问：
- **交互式API文档**: http://localhost:8000/docs
- **ReDoc文档**: http://localhost:8000/redoc

## 测试API

您可以使用`/docs`的交互式文档测试API，或使用curl：

```bash
# 健康检查
curl http://localhost:8000/health

# 获取所有课程（公开端点）
curl http://localhost:8000/courses/all
```

## 示例数据

运行`init_db.py`后，您将拥有这些测试账户：

- **管理员**: `admin` / `admin123`
- **教师**: `teacher` / `teacher123`
- **学生**: `student1`, `student2` / `student123`

## 下一步

1. **探索API**: 使用`/docs`的交互式文档
2. **设置Ollama**: 按照[Ollama设置指南](OLLAMA_SETUP.md)配置AI功能
3. **构建前端**: 开始构建您的前端应用程序
4. **部署**: 按照[部署指南](DEPLOYMENT.md)进行生产部署

## 故障排除

### 常见问题

1. **端口已被占用**: 在`run.py`中更改端口或终止使用端口8000的进程
2. **数据库错误**: 确保您成功运行了`init_db.py`
3. **导入错误**: 确保您在虚拟环境中且所有依赖都已安装

### 获取帮助

- 查看[API文档](http://localhost:8000/docs)
- 查看[Issues](https://github.com/your-username/suma-lms/issues)页面
- 创建新issue并提供详细信息

---

**编码愉快！🚀**
