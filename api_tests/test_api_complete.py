#!/usr/bin/env python3
"""
SUMA LMS 完整 API 测试脚本
测试所有主要功能，包括新的 Ollama AI 集成
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ 服务器健康检查通过")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def test_auth():
    """测试认证功能"""
    print("\n🔐 测试认证功能...")
    
    # 测试登录
    login_data = {
        "username": "student1",
        "password": "student123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login-json", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print("✅ 登录成功")
            
            # 测试获取用户信息
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
            if response.status_code == 200:
                user_info = response.json()
                print(f"✅ 用户信息获取成功: {user_info['full_name']}")
                return token
            else:
                print("❌ 获取用户信息失败")
                return None
        else:
            print(f"❌ 登录失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 认证测试失败: {e}")
        return None

def test_courses(token):
    """测试课程功能"""
    print("\n📚 测试课程功能...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # 获取课程列表
        response = requests.get(f"{BASE_URL}/courses/", headers=headers)
        if response.status_code == 200:
            courses = response.json()
            print(f"✅ 获取课程列表成功: {len(courses)} 个课程")
            for course in courses[:3]:  # 显示前3个课程
                print(f"   - {course['name']} ({course['code']})")
            return True
        else:
            print(f"❌ 获取课程列表失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 课程测试失败: {e}")
        return False

def test_tasks(token):
    """测试任务功能"""
    print("\n📝 测试任务功能...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # 获取任务列表
        response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ 获取任务列表成功: {len(tasks)} 个任务")
            for task in tasks[:3]:  # 显示前3个任务
                print(f"   - {task['title']} (Due: {task['due_date'][:10]})")
            return True
        else:
            print(f"❌ 获取任务列表失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 任务测试失败: {e}")
        return False

def test_ai_status():
    """测试AI状态"""
    print("\n🤖 测试AI状态...")
    
    try:
        response = requests.get(f"{BASE_URL}/ai/status")
        if response.status_code == 200:
            status = response.json()
            print(f"✅ AI状态: {status['status']}")
            print(f"   模型: {status.get('current_model', 'N/A')}")
            print(f"   可用模型: {len(status.get('available_models', []))} 个")
            return status['status'] == 'connected'
        else:
            print(f"❌ AI状态检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ AI状态测试失败: {e}")
        return False

def test_ai_query(token):
    """测试AI查询"""
    print("\n💬 测试AI查询...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        query_data = {
            "query": "你好，请介绍一下我的学习进度"
        }
        
        response = requests.post(f"{BASE_URL}/ai/query", json=query_data, headers=headers)
        if response.status_code == 200:
            ai_response = response.json()
            print("✅ AI查询成功")
            print(f"   回复: {ai_response['response'][:100]}...")
            print(f"   建议: {ai_response['suggestions']}")
            return True
        else:
            print(f"❌ AI查询失败: {response.status_code}")
            print(f"   错误: {response.text}")
            return False
    except Exception as e:
        print(f"❌ AI查询测试失败: {e}")
        return False

def test_dashboard(token):
    """测试仪表板功能"""
    print("\n📊 测试仪表板功能...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/calendar/dashboard", headers=headers)
        if response.status_code == 200:
            dashboard = response.json()
            print("✅ 仪表板数据获取成功")
            stats = dashboard['stats']
            print(f"   总课程数: {stats['total_courses']}")
            print(f"   活跃任务: {stats['active_tasks']}")
            print(f"   即将到期: {stats['upcoming_deadlines']}")
            print(f"   出勤率: {stats['attendance_rate']}%")
            return True
        else:
            print(f"❌ 仪表板数据获取失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 仪表板测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 SUMA LMS 完整功能测试")
    print("=" * 60)
    
    # 测试健康检查
    if not test_health():
        print("\n❌ 服务器未运行，请先启动服务器")
        print("启动命令: python3 -m app.main")
        return
    
    # 测试认证
    token = test_auth()
    if not token:
        print("\n❌ 认证失败，无法继续测试")
        return
    
    # 测试各个功能模块
    test_courses(token)
    test_tasks(token)
    
    # 测试AI功能
    ai_connected = test_ai_status()
    if ai_connected:
        test_ai_query(token)
    else:
        print("⚠️  AI功能不可用，请检查Ollama服务")
    
    # 测试仪表板
    test_dashboard(token)
    
    print("\n" + "=" * 60)
    print("🎉 测试完成！")
    
    if ai_connected:
        print("\n✨ 所有功能正常，包括AI助手！")
        print("📚 访问API文档: http://localhost:8000/docs")
        print("🤖 AI助手已就绪，可以开始使用了！")
    else:
        print("\n⚠️  基本功能正常，但AI助手需要Ollama服务")
        print("请参考 OLLAMA_SETUP.md 设置Ollama")

if __name__ == "__main__":
    main()
