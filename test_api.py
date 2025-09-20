#!/usr/bin/env python3
"""
Simple API test script for SUMA LMS
This script tests basic API functionality
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print("✅ Health check passed")
        return True
    else:
        print("❌ Health check failed")
        return False

def test_register_and_login():
    """Test user registration and login"""
    print("\n🔍 Testing user registration and login...")
    
    # Test registration
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "testpass123",
        "role": "student"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    if response.status_code == 200:
        print("✅ User registration successful")
    else:
        print(f"❌ User registration failed: {response.text}")
        return None
    
    # Test login
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login-json", json=login_data)
    if response.status_code == 200:
        token_data = response.json()
        print("✅ User login successful")
        return token_data["access_token"]
    else:
        print(f"❌ User login failed: {response.text}")
        return None

def test_protected_endpoint(token):
    """Test protected endpoint with authentication"""
    print("\n🔍 Testing protected endpoint...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    
    if response.status_code == 200:
        user_info = response.json()
        print(f"✅ Protected endpoint access successful")
        print(f"   User: {user_info['full_name']} ({user_info['username']})")
        return True
    else:
        print(f"❌ Protected endpoint access failed: {response.text}")
        return False

def test_courses_endpoint(token):
    """Test courses endpoint"""
    print("\n🔍 Testing courses endpoint...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/courses/", headers=headers)
    
    if response.status_code == 200:
        courses = response.json()
        print(f"✅ Courses endpoint successful - Found {len(courses)} courses")
        return True
    else:
        print(f"❌ Courses endpoint failed: {response.text}")
        return False

def test_tasks_endpoint(token):
    """Test tasks endpoint"""
    print("\n🔍 Testing tasks endpoint...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"✅ Tasks endpoint successful - Found {len(tasks)} tasks")
        return True
    else:
        print(f"❌ Tasks endpoint failed: {response.text}")
        return False

def test_dashboard_endpoint(token):
    """Test dashboard endpoint"""
    print("\n🔍 Testing dashboard endpoint...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/calendar/dashboard", headers=headers)
    
    if response.status_code == 200:
        dashboard = response.json()
        print("✅ Dashboard endpoint successful")
        print(f"   Stats: {dashboard['stats']}")
        return True
    else:
        print(f"❌ Dashboard endpoint failed: {response.text}")
        return False

def main():
    """Run all tests"""
    print("🧪 SUMA LMS API Test Suite")
    print("=" * 50)
    
    # Test health endpoint
    if not test_health():
        print("\n❌ Server is not running. Please start the server first:")
        print("   python run.py")
        return
    
    # Test authentication
    token = test_register_and_login()
    if not token:
        print("\n❌ Authentication tests failed")
        return
    
    # Test protected endpoints
    test_protected_endpoint(token)
    test_courses_endpoint(token)
    test_tasks_endpoint(token)
    test_dashboard_endpoint(token)
    
    print("\n" + "=" * 50)
    print("🎉 API tests completed!")
    print("\n📚 You can now explore the API at:")
    print(f"   {BASE_URL}/docs")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the API server.")
        print("   Please make sure the server is running:")
        print("   python run.py")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
