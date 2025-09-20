#!/usr/bin/env python3
"""
Ollama 连接测试脚本
测试 Ollama 服务是否正常运行
"""

import requests
import json
import sys

OLLAMA_BASE_URL = "http://localhost:11434"

def test_ollama_connection():
    """测试 Ollama 连接"""
    print("🔍 测试 Ollama 连接...")
    
    try:
        # 测试基本连接
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama 服务正在运行")
            
            # 获取可用模型
            models = response.json()
            if 'models' in models and models['models']:
                print(f"📦 可用模型: {len(models['models'])} 个")
                for model in models['models']:
                    print(f"   - {model['name']}")
            else:
                print("⚠️  没有找到已下载的模型")
                print("   请运行: ollama pull llama3.2")
                return False
            
            return True
        else:
            print(f"❌ Ollama 服务响应错误: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到 Ollama 服务")
        print("   请确保 Ollama 正在运行: ollama serve")
        return False
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False

def test_model_chat():
    """测试模型聊天功能"""
    print("\n🤖 测试模型聊天功能...")
    
    try:
        # 测试聊天 API
        chat_data = {
            "model": "llama3.1:8b",
            "messages": [
                {
                    "role": "user",
                    "content": "你好，请简单介绍一下你自己。"
                }
            ],
            "stream": False
        }
        
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=chat_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'message' in result and 'content' in result['message']:
                print("✅ 模型聊天功能正常")
                print(f"   回复: {result['message']['content'][:100]}...")
                return True
            else:
                print("❌ 模型响应格式错误")
                return False
        else:
            print(f"❌ 聊天测试失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 聊天测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 Ollama 连接测试")
    print("=" * 50)
    
    # 测试连接
    if not test_ollama_connection():
        print("\n❌ Ollama 设置不完整")
        print("\n请按照以下步骤设置 Ollama:")
        print("1. 安装 Ollama: https://ollama.ai")
        print("2. 启动服务: ollama serve")
        print("3. 下载模型: ollama pull llama3.2")
        sys.exit(1)
    
    # 测试聊天
    if not test_model_chat():
        print("\n❌ 模型聊天功能异常")
        print("请检查模型是否正确下载")
        sys.exit(1)
    
    print("\n🎉 Ollama 设置完成！")
    print("现在可以启动 SUMA LMS 并使用 AI 功能了")
    print("\n启动命令:")
    print("python3 -m app.main")

if __name__ == "__main__":
    main()
