#!/bin/bash

# SUMA LMS 开发环境启动脚本

echo "🚀 启动 SUMA LMS 开发环境..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python 3.8+"
    exit 1
fi

# 检查Node.js环境
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装Node.js 18+"
    exit 1
fi

# 检查Ollama
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama 未安装，AI功能将不可用"
    echo "   请访问 https://ollama.ai 安装Ollama"
fi

# 创建虚拟环境（如果不存在）
if [ ! -d ".venv" ]; then
    echo "📦 创建Python虚拟环境..."
    python3 -m venv .venv
fi

# 激活虚拟环境
echo "🔧 激活Python虚拟环境..."
source .venv/bin/activate

# 安装Python依赖
echo "📦 安装Python依赖..."
pip install -r requirements.txt

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "📝 创建环境变量文件..."
    cp env.example .env
    echo "   请编辑 .env 文件配置您的设置"
fi

# 初始化数据库
echo "🗄️  初始化数据库..."
python init_db.py

# 安装前端依赖
echo "📦 安装前端依赖..."
cd frontend
npm install
cd ..

# 启动Ollama（如果已安装）
if command -v ollama &> /dev/null; then
    echo "🤖 启动Ollama服务..."
    ollama serve &
    OLLAMA_PID=$!
    
    # 等待Ollama启动
    sleep 5
    
    # 拉取模型（如果不存在）
    echo "📥 检查AI模型..."
    ollama list | grep -q "llama3.1:8b" || ollama pull llama3.1:8b
fi

# 启动后端服务
echo "🔧 启动后端服务..."
python -m app.main &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端服务
echo "🎨 启动前端服务..."
cd frontend
npm run dev &
FRONTEND_PID=$!

# 等待前端启动
sleep 3

echo ""
echo "✅ SUMA LMS 开发环境已启动！"
echo ""
echo "🌐 前端: http://localhost:3000"
echo "🔧 后端API: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/api/docs"
echo "🤖 Ollama: http://localhost:11434"
echo ""
echo "测试账户:"
echo "  - 管理员: admin/admin123"
echo "  - 教师: teacher/teacher123"
echo "  - 学生: student1/student123"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
trap "echo '🛑 停止服务...'; kill $BACKEND_PID $FRONTEND_PID $OLLAMA_PID 2>/dev/null; exit" INT
wait
